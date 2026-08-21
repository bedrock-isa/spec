use bedrock_bus::Bus;
use bedrock_core::{
    CPU_REGISTER_INFOS, CpuRegister, CpuRegisterInfo, CpuRegisterSet, StepResult, Trap,
};
use bedrock_debug::Debugger;
use bedrock_machine::{ElfLoadOptions, Machine};
use bedrock_toolchain::BEDROCK_TRIPLE;
use std::fmt::Write as FmtWrite;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream, ToSocketAddrs};
use std::sync::mpsc::{Receiver, TryRecvError};
use std::thread;
use std::time::{Duration, Instant};
use thiserror::Error;

const THREAD_ID: &str = "1";
const MAX_PACKET_SIZE: usize = 4096;
const CONTINUE_UPDATE_INTERVAL: Duration = Duration::from_millis(33);

#[derive(Debug, Error)]
pub enum RemoteError {
    #[error("remote I/O error: {0}")]
    Io(#[from] std::io::Error),
    #[error("remote session cancelled before debugger connected")]
    Cancelled,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PacketResponse {
    pub payload: String,
    pub console_output: Vec<String>,
    pub disconnect: bool,
    pub enable_no_ack: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct RemoteSessionConfig {
    pub reset_image: Option<ResetImage>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ResetImage {
    pub bytes: Vec<u8>,
    pub load_base: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HostControl {
    PushKeyboardEvent(u32),
    Interrupt,
}

impl PacketResponse {
    fn ok(payload: impl Into<String>) -> Self {
        Self {
            payload: payload.into(),
            console_output: Vec::new(),
            disconnect: false,
            enable_no_ack: false,
        }
    }

    fn ok_with_console_output(payload: impl Into<String>, output: impl Into<String>) -> Self {
        Self {
            payload: payload.into(),
            console_output: vec![output.into()],
            disconnect: false,
            enable_no_ack: false,
        }
    }

    fn disconnect(payload: impl Into<String>) -> Self {
        Self {
            payload: payload.into(),
            console_output: Vec::new(),
            disconnect: true,
            enable_no_ack: false,
        }
    }

    fn enable_no_ack() -> Self {
        Self {
            payload: "OK".to_owned(),
            console_output: Vec::new(),
            disconnect: false,
            enable_no_ack: true,
        }
    }
}

pub fn run_tcp<A: ToSocketAddrs>(
    addr: A,
    machine: &mut Machine,
    debugger: &mut Debugger,
) -> Result<(), RemoteError> {
    let listener = TcpListener::bind(addr)?;
    run_tcp_listener(listener, machine, debugger)
}

pub fn run_tcp_listener(
    listener: TcpListener,
    machine: &mut Machine,
    debugger: &mut Debugger,
) -> Result<(), RemoteError> {
    let (stream, peer) = listener.accept()?;
    tracing::info!(?peer, "accepted gdb-remote debugger connection");
    RemoteConnection::new(stream, machine, debugger).run()
}

pub trait RemoteObserver {
    fn machine_updated(&mut self, machine: &Machine, debugger: &Debugger);
}

impl<F> RemoteObserver for F
where
    F: FnMut(&Machine, &Debugger),
{
    fn machine_updated(&mut self, machine: &Machine, debugger: &Debugger) {
        self(machine, debugger);
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub struct NoopRemoteObserver;

impl RemoteObserver for NoopRemoteObserver {
    fn machine_updated(&mut self, _machine: &Machine, _debugger: &Debugger) {}
}

pub fn run_tcp_listener_with_observer<O: RemoteObserver>(
    listener: TcpListener,
    machine: &mut Machine,
    debugger: &mut Debugger,
    observer: O,
) -> Result<(), RemoteError> {
    run_tcp_listener_with_observer_until(listener, machine, debugger, observer, || false)
}

pub fn run_tcp_listener_with_observer_until<O, F>(
    listener: TcpListener,
    machine: &mut Machine,
    debugger: &mut Debugger,
    observer: O,
    mut should_cancel: F,
) -> Result<(), RemoteError>
where
    O: RemoteObserver,
    F: FnMut() -> bool,
{
    run_tcp_listener_configured_with_observer_until(
        listener,
        machine,
        debugger,
        RemoteSessionConfig::default(),
        None,
        observer,
        &mut should_cancel,
    )
}

pub fn run_tcp_listener_configured_with_observer_until<O, F>(
    listener: TcpListener,
    machine: &mut Machine,
    debugger: &mut Debugger,
    config: RemoteSessionConfig,
    host_control_receiver: Option<Receiver<HostControl>>,
    observer: O,
    mut should_cancel: F,
) -> Result<(), RemoteError>
where
    O: RemoteObserver,
    F: FnMut() -> bool,
{
    listener.set_nonblocking(true)?;
    loop {
        match listener.accept() {
            Ok((stream, peer)) => {
                stream.set_nonblocking(false)?;
                tracing::info!(?peer, "accepted gdb-remote debugger connection");
                return RemoteConnection::with_config_and_observer(
                    stream,
                    machine,
                    debugger,
                    config,
                    host_control_receiver,
                    observer,
                )
                .run();
            }
            Err(error) if error.kind() == std::io::ErrorKind::WouldBlock => {
                if should_cancel() {
                    return Err(RemoteError::Cancelled);
                }
                thread::sleep(Duration::from_millis(50));
            }
            Err(error) => return Err(error.into()),
        }
    }
}

struct RemoteConnection<'a, O: RemoteObserver = NoopRemoteObserver> {
    stream: TcpStream,
    protocol: RemoteProtocol<'a, O>,
    no_ack: bool,
}

impl<'a> RemoteConnection<'a, NoopRemoteObserver> {
    fn new(stream: TcpStream, machine: &'a mut Machine, debugger: &'a mut Debugger) -> Self {
        Self::with_observer(stream, machine, debugger, NoopRemoteObserver)
    }
}

impl<'a, O: RemoteObserver> RemoteConnection<'a, O> {
    fn with_observer(
        stream: TcpStream,
        machine: &'a mut Machine,
        debugger: &'a mut Debugger,
        observer: O,
    ) -> Self {
        Self::with_config_and_observer(
            stream,
            machine,
            debugger,
            RemoteSessionConfig::default(),
            None,
            observer,
        )
    }

    fn with_config_and_observer(
        stream: TcpStream,
        machine: &'a mut Machine,
        debugger: &'a mut Debugger,
        config: RemoteSessionConfig,
        host_control_receiver: Option<Receiver<HostControl>>,
        observer: O,
    ) -> Self {
        Self {
            stream,
            protocol: RemoteProtocol::with_config_and_observer(
                machine,
                debugger,
                config,
                host_control_receiver,
                observer,
            ),
            no_ack: false,
        }
    }

    fn run(&mut self) -> Result<(), RemoteError> {
        loop {
            match read_incoming(&mut self.stream, self.no_ack)? {
                Incoming::Interrupt => {
                    let reply = signal_stop_reply(2);
                    write_packet(&mut self.stream, reply.as_bytes())?;
                }
                Incoming::Packet(payload) => {
                    let response = self.protocol.handle_packet(&payload);
                    for output in response.console_output {
                        let packet = format!("O{}", hex_encode(output.as_bytes()));
                        write_packet(&mut self.stream, packet.as_bytes())?;
                    }
                    write_packet(&mut self.stream, response.payload.as_bytes())?;
                    if response.enable_no_ack {
                        self.no_ack = true;
                    }
                    if response.disconnect {
                        return Ok(());
                    }
                }
            }
        }
    }
}

pub struct RemoteProtocol<'a, O: RemoteObserver = NoopRemoteObserver> {
    machine: &'a mut Machine,
    debugger: &'a mut Debugger,
    config: RemoteSessionConfig,
    host_control_receiver: Option<Receiver<HostControl>>,
    observer: O,
    last_streamed_update: Instant,
}

impl<'a> RemoteProtocol<'a, NoopRemoteObserver> {
    pub fn new(machine: &'a mut Machine, debugger: &'a mut Debugger) -> Self {
        Self::with_observer(machine, debugger, NoopRemoteObserver)
    }
}

impl<'a, O: RemoteObserver> RemoteProtocol<'a, O> {
    pub fn with_observer(
        machine: &'a mut Machine,
        debugger: &'a mut Debugger,
        observer: O,
    ) -> Self {
        Self::with_config_and_observer(
            machine,
            debugger,
            RemoteSessionConfig::default(),
            None,
            observer,
        )
    }

    pub fn with_config_and_observer(
        machine: &'a mut Machine,
        debugger: &'a mut Debugger,
        config: RemoteSessionConfig,
        host_control_receiver: Option<Receiver<HostControl>>,
        observer: O,
    ) -> Self {
        Self {
            machine,
            debugger,
            config,
            host_control_receiver,
            observer,
            last_streamed_update: Instant::now(),
        }
    }

    pub fn handle_packet(&mut self, packet: &str) -> PacketResponse {
        if self.drain_host_controls() {
            return PacketResponse::ok(signal_stop_reply(2));
        }

        if packet.is_empty() {
            return PacketResponse::ok("");
        }

        if packet == "!" {
            return PacketResponse::ok("OK");
        }
        if packet == "?" {
            return PacketResponse::ok(stop_reply(&StepResult::Breakpoint));
        }
        if packet == "QStartNoAckMode" {
            return PacketResponse::enable_no_ack();
        }
        if packet.starts_with("qSupported") {
            return PacketResponse::ok(
                "PacketSize=1000;QStartNoAckMode+;qXfer:features:read+;swbreak+;vContSupported+",
            );
        }
        if packet == "qAttached" {
            return PacketResponse::ok("1");
        }
        if packet == "qC" {
            return PacketResponse::ok(format!("QC{THREAD_ID}"));
        }
        if packet == "qfThreadInfo" {
            return PacketResponse::ok(format!("m{THREAD_ID}"));
        }
        if packet == "qsThreadInfo" {
            return PacketResponse::ok("l");
        }
        if let Some(thread_id) = packet.strip_prefix("qThreadExtraInfo,") {
            return if thread_id == THREAD_ID {
                PacketResponse::ok(hex_encode(b"bedrock-cpu"))
            } else {
                PacketResponse::ok("E45")
            };
        }
        if packet == "qHostInfo" {
            return PacketResponse::ok(host_info());
        }
        if packet == "qProcessInfo" {
            return PacketResponse::ok(process_info());
        }
        if let Some(command) = packet.strip_prefix("qRcmd,") {
            return self.handle_monitor_command(command);
        }
        if packet == "qOffsets" {
            return PacketResponse::ok("Text=0;Data=0;Bss=0");
        }
        if packet == "qSymbol::" || packet == "QListThreadsInStopReply" {
            return PacketResponse::ok("OK");
        }
        if packet.starts_with("H") || packet.starts_with("T") {
            return PacketResponse::ok("OK");
        }
        if let Some(index) = packet.strip_prefix("qRegisterInfo") {
            return PacketResponse::ok(register_info(index));
        }
        if let Some(query) = packet.strip_prefix("qXfer:features:read:target.xml:") {
            return PacketResponse::ok(read_target_xml(query));
        }
        if packet == "vCont?" {
            return PacketResponse::ok("vCont;c;s");
        }
        if let Some(command) = packet.strip_prefix("vCont;") {
            return self.handle_vcont(command);
        }
        if let Some(command) = packet.strip_prefix('c') {
            return self.continue_execution(command);
        }
        if let Some(command) = packet.strip_prefix('s') {
            return self.single_step(command);
        }
        if packet == "g" {
            return PacketResponse::ok(hex_encode(&self.read_all_registers()));
        }
        if let Some(encoded) = packet.strip_prefix('G') {
            return PacketResponse::ok(self.write_all_registers(encoded));
        }
        if let Some(index) = packet.strip_prefix('p') {
            return PacketResponse::ok(self.read_register(index));
        }
        if let Some(command) = packet.strip_prefix('P') {
            return PacketResponse::ok(self.write_register(command));
        }
        if let Some(command) = packet.strip_prefix('m') {
            return PacketResponse::ok(self.read_memory(command));
        }
        if let Some(command) = packet.strip_prefix('M') {
            return PacketResponse::ok(self.write_memory(command));
        }
        if let Some(command) = packet.strip_prefix("Z0,") {
            return PacketResponse::ok(self.add_breakpoint(command));
        }
        if let Some(command) = packet.strip_prefix("z0,") {
            return PacketResponse::ok(self.remove_breakpoint(command));
        }
        if packet.starts_with('D') {
            return PacketResponse::disconnect("OK");
        }
        if packet.starts_with('k') {
            return PacketResponse::disconnect("");
        }

        PacketResponse::ok("")
    }

    fn handle_vcont(&mut self, command: &str) -> PacketResponse {
        for action in command.split(';') {
            if let Some(rest) = action.strip_prefix('c') {
                return self.continue_execution(vcont_action_suffix(rest));
            }
            if let Some(rest) = action.strip_prefix('s') {
                return self.single_step(vcont_action_suffix(rest));
            }
        }
        PacketResponse::ok("")
    }

    fn handle_monitor_command(&mut self, encoded: &str) -> PacketResponse {
        let Ok(bytes) = hex_decode(encoded) else {
            return PacketResponse::ok_with_console_output("E01", "invalid qRcmd hex payload\n");
        };
        let Ok(raw_command) = std::str::from_utf8(&bytes) else {
            return PacketResponse::ok_with_console_output("E01", "invalid qRcmd utf-8 payload\n");
        };

        let mut parts = raw_command.split_whitespace();
        let Some(command) = parts.next() else {
            return PacketResponse::ok_with_console_output("E01", monitor_help());
        };

        match command {
            "help" | "bedrock-help" => PacketResponse::ok_with_console_output("OK", monitor_help()),
            "processor-reset" | "pr" => {
                let Some(raw_pc) = parts.next() else {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: processor-reset <pc>\n",
                    );
                };
                if parts.next().is_some() {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: processor-reset <pc>\n",
                    );
                }
                let Ok(pc) = parse_hex_u64(raw_pc) else {
                    return PacketResponse::ok_with_console_output("E01", "invalid reset pc\n");
                };

                self.machine.processor_reset(pc);
                self.notify_machine_updated();
                PacketResponse::ok_with_console_output(
                    "OK",
                    format!("processor reset at 0x{pc:016x}\n"),
                )
            }
            "system-reset" | "sr" => {
                let Some(raw_pc) = parts.next() else {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: system-reset <pc>\n",
                    );
                };
                if parts.next().is_some() {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: system-reset <pc>\n",
                    );
                }
                let Ok(pc) = parse_hex_u64(raw_pc) else {
                    return PacketResponse::ok_with_console_output("E01", "invalid reset pc\n");
                };

                match self.system_reset(pc) {
                    Ok(()) => PacketResponse::ok_with_console_output(
                        "OK",
                        format!("system reset at 0x{pc:016x}\n"),
                    ),
                    Err(error) => PacketResponse::ok_with_console_output(
                        "E01",
                        format!("system reset failed: {error}\n"),
                    ),
                }
            }
            "breakpoint-add" | "bp-add" => {
                let Some(raw_addr) = parts.next() else {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: breakpoint-add <addr>\n",
                    );
                };
                if parts.next().is_some() {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: breakpoint-add <addr>\n",
                    );
                }
                let Ok(addr) = parse_hex_u64(raw_addr) else {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "invalid breakpoint address\n",
                    );
                };
                self.debugger.breakpoints_mut().add(addr);
                self.notify_machine_updated();
                PacketResponse::ok_with_console_output(
                    "OK",
                    format!("breakpoint added at 0x{addr:016x}\n"),
                )
            }
            "breakpoint-remove" | "bp-remove" => {
                let Some(raw_addr) = parts.next() else {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: breakpoint-remove <addr>\n",
                    );
                };
                if parts.next().is_some() {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "usage: breakpoint-remove <addr>\n",
                    );
                }
                let Ok(addr) = parse_hex_u64(raw_addr) else {
                    return PacketResponse::ok_with_console_output(
                        "E01",
                        "invalid breakpoint address\n",
                    );
                };
                self.debugger.breakpoints_mut().remove(addr);
                self.notify_machine_updated();
                PacketResponse::ok_with_console_output(
                    "OK",
                    format!("breakpoint removed at 0x{addr:016x}\n"),
                )
            }
            _ => PacketResponse::ok_with_console_output(
                "E01",
                format!(
                    "unknown bedrock monitor command: {command}\n{}",
                    monitor_help()
                ),
            ),
        }
    }

    fn continue_execution(&mut self, command: &str) -> PacketResponse {
        if !command.is_empty()
            && let Ok(pc) = parse_hex_u64(command)
        {
            self.machine.cpu_mut().state_mut().pc = pc;
        }

        if self
            .debugger
            .breakpoints()
            .contains_enabled(self.machine.state().pc)
        {
            let result = self.debugger.step_ignore_breakpoints(self.machine);
            if !matches!(result, StepResult::Running) {
                self.notify_machine_updated();
                return PacketResponse::ok(stop_reply(&result));
            }
            self.notify_machine_updated_if_due();
            if self.drain_host_controls() {
                return PacketResponse::ok(signal_stop_reply(2));
            }
        }

        if self.drain_host_controls() {
            return PacketResponse::ok(signal_stop_reply(2));
        }

        loop {
            let result = self.debugger.run_step(self.machine);
            if !matches!(result, StepResult::Running) {
                self.notify_machine_updated();
                return PacketResponse::ok(stop_reply(&result));
            }
            self.notify_machine_updated_if_due();
            if self.drain_host_controls() {
                return PacketResponse::ok(signal_stop_reply(2));
            }
        }
    }

    fn single_step(&mut self, command: &str) -> PacketResponse {
        if !command.is_empty()
            && let Ok(pc) = parse_hex_u64(command)
        {
            self.machine.cpu_mut().state_mut().pc = pc;
        }
        let result = self.debugger.step_ignore_breakpoints(self.machine);
        self.notify_machine_updated();
        PacketResponse::ok(stop_reply(&result))
    }

    fn read_all_registers(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(register_byte_len());
        for index in 0..CPU_REGISTER_INFOS.len() {
            bytes.extend(self.read_register_bytes(index).unwrap_or_default());
        }
        bytes
    }

    fn write_all_registers(&mut self, encoded: &str) -> String {
        let Ok(bytes) = hex_decode(encoded) else {
            return "E01".to_owned();
        };
        if bytes.len() != register_byte_len() {
            return "E22".to_owned();
        }

        let mut offset = 0;
        for index in 0..CPU_REGISTER_INFOS.len() {
            let size = register_size(index);
            if self
                .write_register_bytes(index, &bytes[offset..offset + size])
                .is_err()
            {
                return "E22".to_owned();
            }
            offset += size;
        }
        self.notify_machine_updated();
        "OK".to_owned()
    }

    fn read_register(&self, raw_index: &str) -> String {
        let Ok(index) = parse_hex_usize(raw_index) else {
            return "E01".to_owned();
        };
        self.read_register_bytes(index)
            .map(|bytes| hex_encode(&bytes))
            .unwrap_or_else(|| "E45".to_owned())
    }

    fn write_register(&mut self, command: &str) -> String {
        let Some((raw_index, raw_value)) = command.split_once('=') else {
            return "E01".to_owned();
        };
        let Ok(index) = parse_hex_usize(raw_index) else {
            return "E01".to_owned();
        };
        let Ok(bytes) = hex_decode(raw_value) else {
            return "E01".to_owned();
        };
        match self.write_register_bytes(index, &bytes) {
            Ok(()) => {
                self.notify_machine_updated();
                "OK".to_owned()
            }
            Err(()) => "E45".to_owned(),
        }
    }

    fn read_register_bytes(&self, index: usize) -> Option<Vec<u8>> {
        let info = CPU_REGISTER_INFOS.get(index)?;
        let state = self.machine.state();
        Some(register_value_bytes(
            state.read_register(info.register),
            info.bits,
        ))
    }

    fn write_register_bytes(&mut self, index: usize, bytes: &[u8]) -> Result<(), ()> {
        let Some(info) = CPU_REGISTER_INFOS.get(index) else {
            return Err(());
        };
        if bytes.len() != register_size(index) {
            return Err(());
        }
        let state = self.machine.cpu_mut().state_mut();
        state.write_register(info.register, read_le_register_value(bytes));
        Ok(())
    }

    fn read_memory(&mut self, command: &str) -> String {
        let Some((raw_addr, raw_len)) = command.split_once(',') else {
            return "E01".to_owned();
        };
        let Ok(addr) = parse_hex_u64(raw_addr) else {
            return "E01".to_owned();
        };
        let Ok(len) = parse_hex_usize(raw_len) else {
            return "E01".to_owned();
        };

        let mut bytes = Vec::with_capacity(len);
        for offset in 0..len {
            let Some(addr) = addr.checked_add(offset as u64) else {
                return "E14".to_owned();
            };
            let Ok(byte) = self.machine.board_mut().read_u8(addr) else {
                return "E14".to_owned();
            };
            bytes.push(byte);
        }
        hex_encode(&bytes)
    }

    fn write_memory(&mut self, command: &str) -> String {
        let Some((range, raw_bytes)) = command.split_once(':') else {
            return "E01".to_owned();
        };
        let Some((raw_addr, raw_len)) = range.split_once(',') else {
            return "E01".to_owned();
        };
        let Ok(addr) = parse_hex_u64(raw_addr) else {
            return "E01".to_owned();
        };
        let Ok(len) = parse_hex_usize(raw_len) else {
            return "E01".to_owned();
        };
        let Ok(bytes) = hex_decode(raw_bytes) else {
            return "E01".to_owned();
        };
        if bytes.len() != len {
            return "E22".to_owned();
        }
        for (offset, byte) in bytes.into_iter().enumerate() {
            let Some(addr) = addr.checked_add(offset as u64) else {
                return "E14".to_owned();
            };
            if self.machine.board_mut().write_u8(addr, byte).is_err() {
                return "E14".to_owned();
            }
        }
        self.notify_machine_updated();
        "OK".to_owned()
    }

    fn add_breakpoint(&mut self, command: &str) -> String {
        let Some((raw_addr, _kind)) = command.split_once(',') else {
            return "E01".to_owned();
        };
        let Ok(addr) = parse_hex_u64(raw_addr) else {
            return "E01".to_owned();
        };
        self.debugger.breakpoints_mut().add(addr);
        self.notify_machine_updated();
        "OK".to_owned()
    }

    fn remove_breakpoint(&mut self, command: &str) -> String {
        let Some((raw_addr, _kind)) = command.split_once(',') else {
            return "E01".to_owned();
        };
        let Ok(addr) = parse_hex_u64(raw_addr) else {
            return "E01".to_owned();
        };
        self.debugger.breakpoints_mut().remove(addr);
        self.notify_machine_updated();
        "OK".to_owned()
    }

    fn system_reset(&mut self, pc: u64) -> Result<(), String> {
        if let Some(image) = &self.config.reset_image {
            let mut machine = Machine::new();
            machine
                .load_elf(
                    &image.bytes,
                    ElfLoadOptions {
                        load_base: image.load_base,
                    },
                )
                .map_err(|error| error.to_string())?;
            machine.processor_reset(pc);
            *self.machine = machine;
        } else {
            self.machine.system_reset(pc);
        }
        self.notify_machine_updated();
        Ok(())
    }

    fn drain_host_controls(&mut self) -> bool {
        let mut interrupted = false;
        let mut updated = false;
        let mut disconnected = false;

        while let Some(receiver) = self.host_control_receiver.as_ref() {
            match receiver.try_recv() {
                Ok(HostControl::PushKeyboardEvent(event)) => {
                    self.machine.board_mut().keyboard_mut().push_event(event);
                    updated = true;
                }
                Ok(HostControl::Interrupt) => {
                    interrupted = true;
                }
                Err(TryRecvError::Empty) => break,
                Err(TryRecvError::Disconnected) => {
                    disconnected = true;
                    break;
                }
            }
        }

        if disconnected {
            self.host_control_receiver = None;
        }
        if updated || interrupted {
            self.notify_machine_updated();
        }

        interrupted
    }

    fn notify_machine_updated(&mut self) {
        self.observer
            .machine_updated(self.machine as &Machine, self.debugger as &Debugger);
        self.last_streamed_update = Instant::now();
    }

    fn notify_machine_updated_if_due(&mut self) {
        if self.last_streamed_update.elapsed() >= CONTINUE_UPDATE_INTERVAL {
            self.notify_machine_updated();
        }
    }
}

enum Incoming {
    Packet(String),
    Interrupt,
}

fn read_incoming(stream: &mut TcpStream, no_ack: bool) -> Result<Incoming, RemoteError> {
    let mut byte = [0u8; 1];
    loop {
        stream.read_exact(&mut byte)?;
        match byte[0] {
            0x03 => return Ok(Incoming::Interrupt),
            b'$' => break,
            _ => {}
        }
    }

    let mut payload = Vec::new();
    let mut checksum = 0u8;
    loop {
        stream.read_exact(&mut byte)?;
        if byte[0] == b'#' {
            break;
        }
        checksum = checksum.wrapping_add(byte[0]);
        payload.push(byte[0]);
        if payload.len() > MAX_PACKET_SIZE {
            if !no_ack {
                stream.write_all(b"-")?;
            }
            return read_incoming(stream, no_ack);
        }
    }

    let mut raw_checksum = [0u8; 2];
    stream.read_exact(&mut raw_checksum)?;
    let expected = (hex_nibble(raw_checksum[0])? << 4) | hex_nibble(raw_checksum[1])?;
    if expected != checksum {
        if !no_ack {
            stream.write_all(b"-")?;
        }
        return read_incoming(stream, no_ack);
    }

    if !no_ack {
        stream.write_all(b"+")?;
    }
    Ok(Incoming::Packet(
        String::from_utf8_lossy(&payload).into_owned(),
    ))
}

fn write_packet(stream: &mut TcpStream, payload: &[u8]) -> Result<(), RemoteError> {
    let checksum = payload
        .iter()
        .fold(0u8, |sum, byte| sum.wrapping_add(*byte));
    stream.write_all(b"$")?;
    stream.write_all(payload)?;
    write!(stream, "#{checksum:02x}")?;
    stream.flush()?;
    Ok(())
}

fn stop_reply(result: &StepResult) -> String {
    match result {
        StepResult::Running => signal_stop_reply(5),
        StepResult::Halted => "W00".to_owned(),
        StepResult::Breakpoint => signal_stop_reply(5),
        StepResult::Trap(trap) => match trap {
            Trap::IllegalInstruction { .. } | Trap::InvalidControlState { .. } => {
                signal_stop_reply(4)
            }
            Trap::DivideError { .. }
            | Trap::FloatingPointFault { .. }
            | Trap::VectorRangeError { .. } => signal_stop_reply(8),
            Trap::Bus { .. } | Trap::AcknowledgedBusFailure { .. } | Trap::PageFault { .. } => {
                signal_stop_reply(11)
            }
            Trap::Decode { .. } | Trap::PrivilegeFault { .. } => signal_stop_reply(5),
        },
    }
}

fn signal_stop_reply(signal: u8) -> String {
    format!("T{signal:02x}thread:{THREAD_ID};")
}

fn host_info() -> String {
    format!(
        "triple:{};endian:little;ptrsize:8;",
        hex_encode(host_triple().as_bytes())
    )
}

fn process_info() -> String {
    format!(
        "pid:1;triple:{};endian:little;ptrsize:8;",
        hex_encode(BEDROCK_TRIPLE.as_bytes())
    )
}

fn monitor_help() -> &'static str {
    "Bedrock monitor commands:\n  processor-reset <pc>\n  system-reset <pc>\n  breakpoint-add <addr>\n  breakpoint-remove <addr>\n"
}

fn host_triple() -> &'static str {
    #[cfg(all(target_os = "macos", target_arch = "aarch64"))]
    {
        "arm64-apple-macosx"
    }

    #[cfg(all(target_os = "macos", target_arch = "x86_64"))]
    {
        "x86_64-apple-macosx"
    }

    #[cfg(all(target_os = "linux", target_arch = "x86_64"))]
    {
        "x86_64-unknown-linux-gnu"
    }

    #[cfg(all(target_os = "linux", target_arch = "aarch64"))]
    {
        "aarch64-unknown-linux-gnu"
    }

    #[cfg(not(any(
        all(target_os = "macos", target_arch = "aarch64"),
        all(target_os = "macos", target_arch = "x86_64"),
        all(target_os = "linux", target_arch = "x86_64"),
        all(target_os = "linux", target_arch = "aarch64")
    )))]
    {
        "unknown-unknown-unknown"
    }
}

fn register_info(raw_index: &str) -> String {
    let Ok(index) = parse_hex_usize(raw_index) else {
        return "E01".to_owned();
    };
    let Some(info) = CPU_REGISTER_INFOS.get(index) else {
        return "E45".to_owned();
    };

    let generic = match info.register {
        CpuRegister::Sp => "generic:sp;",
        CpuRegister::Pc => "generic:pc;",
        CpuRegister::Flags => "generic:flags;",
        _ => "",
    };
    let name = remote_register_name(info);
    format!(
        "name:{};bitsize:{};offset:{};encoding:uint;format:hex;set:{};gcc:{};dwarf:{};{}",
        name,
        info.bits,
        register_offset(index),
        register_set_name(info.set),
        index,
        index,
        generic
    )
}

fn read_target_xml(query: &str) -> String {
    let Some((raw_offset, raw_length)) = query.split_once(',') else {
        return "E01".to_owned();
    };
    let Ok(offset) = parse_hex_usize(raw_offset) else {
        return "E01".to_owned();
    };
    let Ok(length) = parse_hex_usize(raw_length) else {
        return "E01".to_owned();
    };
    let xml = target_xml();
    if offset >= xml.len() {
        return "l".to_owned();
    }

    let end = offset.saturating_add(length).min(xml.len());
    let marker = if end == xml.len() { 'l' } else { 'm' };
    format!("{marker}{}", &xml[offset..end])
}

fn vcont_action_suffix(raw: &str) -> &str {
    raw.split_once(':').map_or(raw, |(addr, _thread)| addr)
}

fn register_size(index: usize) -> usize {
    CPU_REGISTER_INFOS
        .get(index)
        .map(|info| register_size_for_bits(info.bits))
        .unwrap_or(0)
}

fn register_size_for_bits(bits: u16) -> usize {
    usize::from(bits).div_ceil(8)
}

fn register_byte_len() -> usize {
    CPU_REGISTER_INFOS
        .iter()
        .map(|info| register_size_for_bits(info.bits))
        .sum()
}

fn register_offset(index: usize) -> usize {
    CPU_REGISTER_INFOS
        .iter()
        .take(index)
        .map(|info| register_size_for_bits(info.bits))
        .sum()
}

fn register_value_bytes(value: u64, bits: u16) -> Vec<u8> {
    let size = register_size_for_bits(bits);
    value.to_le_bytes()[..size].to_vec()
}

fn read_le_register_value(bytes: &[u8]) -> u64 {
    let mut raw = [0u8; 8];
    raw[..bytes.len()].copy_from_slice(bytes);
    u64::from_le_bytes(raw)
}

fn target_xml() -> String {
    let mut xml = String::from(
        r#"<?xml version="1.0"?>
<!DOCTYPE target SYSTEM "gdb-target.dtd">
<target>
  <architecture>bedrock</architecture>
  <feature name="org.bedrock.cpu">
"#,
    );
    for (index, info) in CPU_REGISTER_INFOS.iter().enumerate() {
        let _ = writeln!(
            xml,
            r#"    <reg name="{}" bitsize="{}" type="{}" regnum="{}"/>"#,
            remote_register_name(info),
            info.bits,
            remote_register_type(info),
            index
        );
    }
    xml.push_str(
        r#"  </feature>
</target>
"#,
    );
    xml
}

fn remote_register_name(info: &CpuRegisterInfo) -> String {
    info.name.to_ascii_lowercase()
}

fn remote_register_type(info: &CpuRegisterInfo) -> &'static str {
    match info.register {
        CpuRegister::Pc => "code_ptr",
        CpuRegister::Sp | CpuRegister::General(_) => "data_ptr",
        _ if info.bits == 16 => "uint16",
        _ if info.bits == 8 => "uint8",
        _ => "uint64",
    }
}

fn register_set_name(set: CpuRegisterSet) -> &'static str {
    match set {
        CpuRegisterSet::General => "General Purpose Registers",
        CpuRegisterSet::Segment => "Segment Registers",
        CpuRegisterSet::Control => "Control Registers",
        CpuRegisterSet::FloatingPoint => "Floating Point Registers",
    }
}

fn parse_hex_u64(raw: &str) -> Result<u64, std::num::ParseIntError> {
    u64::from_str_radix(raw.trim_start_matches("0x"), 16)
}

fn parse_hex_usize(raw: &str) -> Result<usize, std::num::ParseIntError> {
    usize::from_str_radix(raw.trim_start_matches("0x"), 16)
}

fn hex_encode(bytes: &[u8]) -> String {
    let mut encoded = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        encoded.push(hex_char(byte >> 4));
        encoded.push(hex_char(byte & 0x0f));
    }
    encoded
}

fn hex_decode(raw: &str) -> Result<Vec<u8>, ()> {
    let bytes = raw.as_bytes();
    if !bytes.len().is_multiple_of(2) {
        return Err(());
    }

    let mut decoded = Vec::with_capacity(bytes.len() / 2);
    for pair in bytes.chunks_exact(2) {
        decoded.push(
            (hex_nibble(pair[0]).map_err(|_| ())? << 4) | hex_nibble(pair[1]).map_err(|_| ())?,
        );
    }
    Ok(decoded)
}

fn hex_nibble(byte: u8) -> Result<u8, std::io::Error> {
    match byte {
        b'0'..=b'9' => Ok(byte - b'0'),
        b'a'..=b'f' => Ok(byte - b'a' + 10),
        b'A'..=b'F' => Ok(byte - b'A' + 10),
        _ => Err(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            "invalid hex digit",
        )),
    }
}

fn hex_char(nibble: u8) -> char {
    match nibble & 0x0f {
        0..=9 => (b'0' + (nibble & 0x0f)) as char,
        value => (b'a' + value - 10) as char,
    }
}

#[cfg(test)]
mod tests {
    use super::{
        BEDROCK_TRIPLE, HostControl, NoopRemoteObserver, RemoteError, RemoteProtocol,
        RemoteSessionConfig, hex_encode, run_tcp_listener_with_observer_until, stop_reply,
    };
    use bedrock_bus::Bus;
    use bedrock_core::exception::InvalidControlCause;
    use bedrock_core::fpu::env::FpCauses;
    use bedrock_core::{CPU_REGISTER_INFOS, StepResult, Trap, VectorRangeErrorCause};
    use bedrock_debug::Debugger;
    use bedrock_machine::Machine;
    use bedrock_machine::board::{RAM_BASE, RAM_SIZE};
    use std::net::TcpListener;
    use std::sync::mpsc;

    #[test]
    fn reports_lldb_register_metadata() {
        let mut machine = Machine::new();
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        let response = protocol.handle_packet("qRegisterInfo11");

        assert!(response.payload.contains("name:pc;"));
        assert!(response.payload.contains("generic:pc;"));

        let f0_index = register_index("F0");
        let response = protocol.handle_packet(&format!("qRegisterInfo{f0_index:x}"));
        assert!(response.payload.contains("name:f0;"));
        assert!(response.payload.contains("set:Floating Point Registers;"));
    }

    #[test]
    fn reports_lldb_host_and_process_info_without_bedrock_host_triple() {
        let mut machine = Machine::new();
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        let host = protocol.handle_packet("qHostInfo").payload;
        let process = protocol.handle_packet("qProcessInfo").payload;

        assert!(host.contains("triple:"));
        assert!(host.contains("ptrsize:8;"));
        assert!(!host.contains("bedrock"));
        assert_eq!(
            process,
            format!(
                "pid:1;triple:{};endian:little;ptrsize:8;",
                hex_encode(BEDROCK_TRIPLE.as_bytes())
            )
        );
    }

    #[test]
    fn reads_and_writes_registers_little_endian() {
        let mut machine = Machine::new();
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        assert_eq!(protocol.handle_packet("P0=8877665544332211").payload, "OK");
        assert_eq!(
            protocol.handle_packet("p0").payload,
            "8877665544332211".to_owned()
        );
        assert_eq!(protocol.machine.state().r[0], 0x1122_3344_5566_7788);

        let f0_index = register_index("F0");
        assert_eq!(
            protocol
                .handle_packet(&format!("P{f0_index:x}=0807060504030201"))
                .payload,
            "OK"
        );
        assert_eq!(protocol.machine.state().f[0], 0x0102_0304_0506_0708);

        let sss_index = register_index("SSS");
        assert_eq!(
            protocol
                .handle_packet(&format!("P{sss_index:x}=8877665544332211"))
                .payload,
            "OK"
        );
        assert_eq!(protocol.machine.state().sss.raw(), 0x1122_3344_5566_7788);
    }

    fn register_index(name: &str) -> usize {
        CPU_REGISTER_INFOS
            .iter()
            .position(|info| info.name == name)
            .expect("register exists in CpuState metadata")
    }

    #[test]
    fn reads_and_writes_physical_memory() {
        let mut machine = Machine::new();
        machine.load_program(0x100, &[1, 2, 3]).unwrap();
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        assert_eq!(protocol.handle_packet("m100,3").payload, "010203");
        assert_eq!(protocol.handle_packet("M104,3:aabbcc").payload, "OK");
        assert_eq!(protocol.handle_packet("m104,3").payload, "aabbcc");
        assert_eq!(protocol.handle_packet("mffffffffffffffff,1").payload, "E14");
        assert_eq!(
            protocol.handle_packet("Mffffffffffffffff,1:aa").payload,
            "E14"
        );
    }

    #[test]
    fn breakpoints_use_debugger_breakpoint_set() {
        let mut machine = Machine::new();
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        assert_eq!(protocol.handle_packet("Z0,20,2").payload, "OK");
        assert!(protocol.debugger.breakpoints().contains_enabled(0x20));
        assert_eq!(protocol.handle_packet("z0,20,2").payload, "OK");
        assert!(!protocol.debugger.breakpoints().contains_enabled(0x20));
    }

    #[test]
    fn single_step_returns_stop_reply() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0x01]).unwrap();
        machine.processor_reset(0);
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        assert_eq!(protocol.handle_packet("s").payload, "T05thread:1;");
        assert_eq!(protocol.debugger.trace().len(), 1);
        assert_eq!(protocol.debugger.trace()[0].result, StepResult::Running);
    }

    #[test]
    fn invalid_control_state_returns_illegal_instruction_signal() {
        let result = StepResult::Trap(Trap::InvalidControlState {
            pc: 0x10,
            cause: InvalidControlCause::InvalidImage,
        });

        assert_eq!(stop_reply(&result), "T04thread:1;");
    }

    #[test]
    fn floating_point_fault_returns_floating_point_signal() {
        let result = StepResult::Trap(Trap::FloatingPointFault {
            pc: 0x20,
            causes: FpCauses::DZ,
        });

        assert_eq!(stop_reply(&result), "T08thread:1;");
    }

    #[test]
    fn vector_range_fault_returns_floating_point_signal() {
        let result = StepResult::Trap(Trap::VectorRangeError {
            pc: 0x28,
            cause: VectorRangeErrorCause::LaneIndex,
        });

        assert_eq!(stop_reply(&result), "T08thread:1;");
    }

    #[test]
    fn observer_receives_machine_snapshots_after_step_and_continue() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0x01, 0x01]).unwrap();
        machine.processor_reset(0);
        let mut debugger = Debugger::default();
        debugger.breakpoints_mut().add(2);
        let mut updates = Vec::new();

        {
            let mut protocol = RemoteProtocol::with_observer(
                &mut machine,
                &mut debugger,
                |machine: &Machine, debugger: &Debugger| {
                    updates.push((machine.state().pc, debugger.trace().len()));
                },
            );

            assert_eq!(protocol.handle_packet("s").payload, "T05thread:1;");
            assert_eq!(protocol.handle_packet("c").payload, "T05thread:1;");
        }

        assert_eq!(updates, vec![(1, 1), (2, 1)]);
    }

    #[test]
    fn monitor_processor_reset_resets_cpu_and_notifies_observer() {
        let mut machine = Machine::new();
        machine.load_program(0x20, &[0xaa]).unwrap();
        machine.processor_reset(0x20);
        machine.cpu_mut().state_mut().r[0] = 0xfeed;
        let mut debugger = Debugger::default();
        debugger.breakpoints_mut().add(0x20);
        let mut updates = Vec::new();

        {
            let mut protocol = RemoteProtocol::with_observer(
                &mut machine,
                &mut debugger,
                |machine: &Machine, debugger: &Debugger| {
                    updates.push((machine.state().pc, debugger.breakpoints().all().len()));
                },
            );

            let response = protocol.handle_packet(&qrcmd("processor-reset 0x1000"));

            assert_eq!(response.payload, "OK");
            assert_eq!(
                response.console_output,
                vec!["processor reset at 0x0000000000001000\n".to_owned()]
            );
            assert_eq!(protocol.machine.state().pc, 0x1000);
            assert_eq!(protocol.machine.state().sp, RAM_BASE + RAM_SIZE);
            assert_eq!(protocol.machine.state().r[0], 0);
            assert_eq!(protocol.machine.board_mut().read_u8(0x20).unwrap(), 0xaa);
            assert!(protocol.debugger.breakpoints().contains_enabled(0x20));
        }

        assert_eq!(updates, vec![(0x1000, 1)]);
    }

    #[test]
    fn monitor_system_reset_clears_board_state_and_preserves_breakpoints() {
        let mut machine = Machine::new();
        machine
            .board_mut()
            .framebuffer_mut()
            .write_vram_u8(0, 0xaa)
            .unwrap();
        machine.board_mut().keyboard_mut().push_event(0x0001_0041);
        machine.processor_reset(0x20);
        let mut debugger = Debugger::default();
        debugger.breakpoints_mut().add(0x40);
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        let response = protocol.handle_packet(&qrcmd("system-reset 0x1000"));

        assert_eq!(response.payload, "OK");
        assert_eq!(
            response.console_output,
            vec!["system reset at 0x0000000000001000\n".to_owned()]
        );
        assert_eq!(protocol.machine.state().pc, 0x1000);
        assert_eq!(protocol.machine.board().framebuffer().vram()[0], 0);
        assert_eq!(protocol.machine.board().keyboard().queued_len(), 0);
        assert!(protocol.debugger.breakpoints().contains_enabled(0x40));
    }

    #[test]
    fn monitor_breakpoint_commands_update_debugger_set() {
        let mut machine = Machine::new();
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        let add = protocol.handle_packet(&qrcmd("breakpoint-add 0x1000"));
        assert_eq!(add.payload, "OK");
        assert!(protocol.debugger.breakpoints().contains_enabled(0x1000));

        let remove = protocol.handle_packet(&qrcmd("breakpoint-remove 0x1000"));
        assert_eq!(remove.payload, "OK");
        assert!(!protocol.debugger.breakpoints().contains_enabled(0x1000));
    }

    #[test]
    fn host_controls_push_keyboard_events_and_interrupt_continue() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0x4f, 0x0f]).unwrap();
        machine.processor_reset(0);
        let mut debugger = Debugger::default();
        let (sender, receiver) = mpsc::channel();
        sender
            .send(HostControl::PushKeyboardEvent(0x0001_0041))
            .unwrap();
        sender.send(HostControl::Interrupt).unwrap();
        let mut protocol = RemoteProtocol::with_config_and_observer(
            &mut machine,
            &mut debugger,
            RemoteSessionConfig::default(),
            Some(receiver),
            NoopRemoteObserver,
        );

        assert_eq!(protocol.handle_packet("c").payload, "T02thread:1;");
        assert_eq!(protocol.machine.board().keyboard().queued_len(), 1);
    }

    #[test]
    fn monitor_reports_usage_errors() {
        let mut machine = Machine::new();
        let mut debugger = Debugger::default();
        let mut protocol = RemoteProtocol::new(&mut machine, &mut debugger);

        let response = protocol.handle_packet(&qrcmd("processor-reset"));

        assert_eq!(response.payload, "E01");
        assert_eq!(
            response.console_output,
            vec!["usage: processor-reset <pc>\n"]
        );
    }

    fn qrcmd(command: &str) -> String {
        format!("qRcmd,{}", hex_encode(command.as_bytes()))
    }

    #[test]
    #[ignore = "sandbox may disallow loopback listeners"]
    fn listener_can_be_cancelled_before_debugger_connects() {
        let listener = TcpListener::bind(("127.0.0.1", 0)).unwrap();
        let mut machine = Machine::new();
        let mut debugger = Debugger::default();

        let result = run_tcp_listener_with_observer_until(
            listener,
            &mut machine,
            &mut debugger,
            NoopRemoteObserver,
            || true,
        );

        assert!(matches!(result, Err(RemoteError::Cancelled)));
    }
}
