use bedrock_toolchain::BEDROCK_TRIPLE;
use std::ffi::{CStr, CString, NulError};
use std::os::raw::c_char;
use std::path::PathBuf;
use std::ptr;
use std::sync::mpsc::{self, Receiver, RecvTimeoutError, Sender};
use std::thread;
use std::time::Duration;
use thiserror::Error;

const POLL_INTERVAL: Duration = Duration::from_millis(50);

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LldbConfig {
    pub elf_path: Option<PathBuf>,
    pub remote_addr: String,
}

#[derive(Debug)]
pub struct LldbSession {
    command_sender: Sender<WorkerCommand>,
    event_receiver: Receiver<LldbEvent>,
}

impl LldbSession {
    pub fn spawn(config: LldbConfig) -> Result<Self, LldbError> {
        let (command_sender, command_receiver) = mpsc::channel();
        let (event_sender, event_receiver) = mpsc::channel();

        thread::Builder::new()
            .name("bedrock-liblldb-client".to_owned())
            .spawn(move || run_worker(config, command_receiver, event_sender))
            .map_err(LldbError::Spawn)?;

        Ok(Self {
            command_sender,
            event_receiver,
        })
    }

    pub fn send_command(&self, command: impl Into<String>) -> Result<(), LldbError> {
        self.command_sender
            .send(WorkerCommand::Command(command.into()))
            .map_err(|_| LldbError::SessionClosed)
    }

    pub fn interrupt(&self) -> Result<(), LldbError> {
        self.command_sender
            .send(WorkerCommand::Interrupt)
            .map_err(|_| LldbError::SessionClosed)
    }

    pub fn detach(&self) -> Result<(), LldbError> {
        self.command_sender
            .send(WorkerCommand::Detach)
            .map_err(|_| LldbError::SessionClosed)
    }

    pub fn try_event(&self) -> Option<LldbEvent> {
        self.event_receiver.try_recv().ok()
    }
}

impl Drop for LldbSession {
    fn drop(&mut self) {
        let _ = self.command_sender.send(WorkerCommand::Shutdown);
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LldbEvent {
    Connected { remote_addr: String },
    CommandResult(CommandResult),
    ProcessState(ProcessState),
    Exited { result: Result<(), String> },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CommandResult {
    pub command: String,
    pub output: String,
    pub error: String,
    pub status: i32,
    pub succeeded: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProcessState {
    Invalid,
    Unloaded,
    Connected,
    Attaching,
    Launching,
    Stopped,
    Running,
    Stepping,
    Crashed,
    Detached,
    Exited,
    Suspended,
    Unknown(i32),
}

impl ProcessState {
    fn from_raw(raw: i32) -> Self {
        match raw {
            0 => Self::Invalid,
            1 => Self::Unloaded,
            2 => Self::Connected,
            3 => Self::Attaching,
            4 => Self::Launching,
            5 => Self::Stopped,
            6 => Self::Running,
            7 => Self::Stepping,
            8 => Self::Crashed,
            9 => Self::Detached,
            10 => Self::Exited,
            11 => Self::Suspended,
            value => Self::Unknown(value),
        }
    }
}

#[derive(Debug, Error)]
pub enum LldbError {
    #[error("failed to spawn LLDB worker thread: {0}")]
    Spawn(std::io::Error),
    #[error("LLDB session is closed")]
    SessionClosed,
    #[error("LLDB string argument contains a NUL byte: {0}")]
    Nul(#[from] NulError),
    #[error("{0}")]
    Native(String),
}

#[derive(Debug)]
enum WorkerCommand {
    Command(String),
    Interrupt,
    Detach,
    Shutdown,
}

fn run_worker(
    config: LldbConfig,
    command_receiver: Receiver<WorkerCommand>,
    event_sender: Sender<LldbEvent>,
) {
    let mut native = match NativeSession::connect(&config) {
        Ok(native) => native,
        Err(error) => {
            let _ = event_sender.send(LldbEvent::Exited {
                result: Err(error.to_string()),
            });
            return;
        }
    };
    wait_for_initial_stop(&mut native);

    let _ = event_sender.send(LldbEvent::Connected {
        remote_addr: config.remote_addr.clone(),
    });
    let mut last_state = native.process_state();
    let _ = event_sender.send(LldbEvent::ProcessState(last_state));

    loop {
        match command_receiver.recv_timeout(POLL_INTERVAL) {
            Ok(WorkerCommand::Command(command)) => {
                let should_exit = is_exit_command(&command);
                let result = run_expanded_command(&mut native, &command);
                let _ = event_sender.send(LldbEvent::CommandResult(result));
                if should_exit {
                    let _ = event_sender.send(LldbEvent::Exited { result: Ok(()) });
                    break;
                }
            }
            Ok(WorkerCommand::Interrupt) => {
                let result = native
                    .interrupt()
                    .map(|_| ())
                    .map_err(|err| err.to_string());
                let _ = event_sender.send(LldbEvent::CommandResult(CommandResult {
                    command: "interrupt".to_owned(),
                    output: String::new(),
                    error: result.as_ref().err().cloned().unwrap_or_default(),
                    status: 0,
                    succeeded: result.is_ok(),
                }));
            }
            Ok(WorkerCommand::Detach) | Ok(WorkerCommand::Shutdown) => {
                let result = native.detach().map(|_| ()).map_err(|err| err.to_string());
                let _ = event_sender.send(LldbEvent::Exited { result });
                break;
            }
            Err(RecvTimeoutError::Timeout) => {}
            Err(RecvTimeoutError::Disconnected) => break,
        }

        let state = native.process_state();
        if state != last_state {
            last_state = state;
            let _ = event_sender.send(LldbEvent::ProcessState(state));
        }
    }
}

fn wait_for_initial_stop(native: &mut NativeSession) {
    for attempt in 0..200 {
        match native.process_state() {
            ProcessState::Stopped
            | ProcessState::Crashed
            | ProcessState::Detached
            | ProcessState::Exited => return,
            _ => {
                if attempt == 100 {
                    let _ = native.interrupt();
                }
                thread::sleep(Duration::from_millis(10));
            }
        }
    }
}

fn run_expanded_command(native: &mut NativeSession, command: &str) -> CommandResult {
    let expanded = match expand_command(command) {
        Ok(commands) => commands,
        Err(error) => {
            return CommandResult {
                command: command.to_owned(),
                output: String::new(),
                error,
                status: 0,
                succeeded: false,
            };
        }
    };

    let mut output = String::new();
    let mut error = String::new();
    let mut status = 0;
    let mut succeeded = true;

    for expanded_command in expanded {
        match native.command(&expanded_command) {
            Ok(result) => {
                status = result.status;
                succeeded &= result.succeeded;
                output.push_str(&result.output);
                error.push_str(&result.error);
            }
            Err(err) => {
                succeeded = false;
                error.push_str(&err.to_string());
                error.push('\n');
            }
        }
    }

    CommandResult {
        command: command.to_owned(),
        output,
        error,
        status,
        succeeded,
    }
}

fn expand_command(command: &str) -> Result<Vec<String>, String> {
    let trimmed = command.trim();
    let mut parts = trimmed.split_whitespace();
    let Some(head) = parts.next() else {
        return Ok(vec![String::new()]);
    };

    match head {
        "br-pr" => {
            let pc = one_arg(parts, "usage: br-pr <pc>")?;
            Ok(vec![
                format!("process plugin packet monitor processor-reset {pc}"),
                format!("register write pc {pc}"),
            ])
        }
        "br-reset" => {
            let pc = one_arg(parts, "usage: br-reset <pc>")?;
            Ok(vec![
                format!("process plugin packet monitor system-reset {pc}"),
                format!("register write pc {pc}"),
            ])
        }
        "br-help" => {
            if parts.next().is_some() {
                return Err("usage: br-help".to_owned());
            }
            Ok(vec![
                "process plugin packet monitor bedrock-help".to_owned(),
            ])
        }
        _ => Ok(vec![trimmed.to_owned()]),
    }
}

fn one_arg<'a>(
    mut parts: impl Iterator<Item = &'a str>,
    usage: &'static str,
) -> Result<&'a str, String> {
    let Some(arg) = parts.next() else {
        return Err(usage.to_owned());
    };
    if parts.next().is_some() {
        return Err(usage.to_owned());
    }
    Ok(arg)
}

fn is_exit_command(command: &str) -> bool {
    matches!(command.trim(), "detach" | "quit" | "q")
}

#[derive(Debug)]
struct NativeSession {
    raw: *mut ffi::BedrockLldbSession,
}

impl NativeSession {
    fn connect(config: &LldbConfig) -> Result<Self, LldbError> {
        let elf_path = config
            .elf_path
            .as_ref()
            .map(|path| CString::new(path.display().to_string()))
            .transpose()?;
        let triple = CString::new(BEDROCK_TRIPLE)?;
        let remote_url = CString::new(format!("connect://{}", config.remote_addr))?;
        let mut error = ptr::null_mut();

        let raw = unsafe {
            ffi::bedrock_lldb_connect(
                elf_path.as_ref().map_or(ptr::null(), |path| path.as_ptr()),
                triple.as_ptr(),
                remote_url.as_ptr(),
                &mut error,
            )
        };

        if raw.is_null() {
            return Err(LldbError::Native(unsafe { take_string(error) }));
        }

        Ok(Self { raw })
    }

    fn command(&mut self, command: &str) -> Result<CommandResult, LldbError> {
        let command_cstr = CString::new(command)?;
        let mut status = 0;
        let mut succeeded = 0;
        let mut output = ptr::null_mut();
        let mut error = ptr::null_mut();

        let ok = unsafe {
            ffi::bedrock_lldb_command(
                self.raw,
                command_cstr.as_ptr(),
                &mut status,
                &mut succeeded,
                &mut output,
                &mut error,
            )
        };

        let output = unsafe { take_string(output) };
        let error = unsafe { take_string(error) };

        if ok == 0 {
            return Err(LldbError::Native(error));
        }

        Ok(CommandResult {
            command: command.to_owned(),
            output,
            error,
            status,
            succeeded: succeeded != 0,
        })
    }

    fn interrupt(&mut self) -> Result<(), LldbError> {
        let mut error = ptr::null_mut();
        let ok = unsafe { ffi::bedrock_lldb_interrupt(self.raw, &mut error) };
        if ok == 0 {
            return Err(LldbError::Native(unsafe { take_string(error) }));
        }
        Ok(())
    }

    fn detach(&mut self) -> Result<(), LldbError> {
        let mut error = ptr::null_mut();
        let ok = unsafe { ffi::bedrock_lldb_detach(self.raw, &mut error) };
        if ok == 0 {
            return Err(LldbError::Native(unsafe { take_string(error) }));
        }
        Ok(())
    }

    fn process_state(&self) -> ProcessState {
        ProcessState::from_raw(unsafe { ffi::bedrock_lldb_process_state(self.raw) })
    }
}

impl Drop for NativeSession {
    fn drop(&mut self) {
        unsafe {
            ffi::bedrock_lldb_destroy(self.raw);
        }
    }
}

unsafe fn take_string(raw: *mut c_char) -> String {
    if raw.is_null() {
        return String::new();
    }
    let value = unsafe { CStr::from_ptr(raw) }
        .to_string_lossy()
        .into_owned();
    unsafe {
        ffi::bedrock_lldb_string_free(raw);
    }
    value
}

mod ffi {
    use std::os::raw::{c_char, c_int};

    #[repr(C)]
    pub struct BedrockLldbSession {
        _private: [u8; 0],
    }

    unsafe extern "C" {
        pub fn bedrock_lldb_connect(
            elf_path: *const c_char,
            target_triple: *const c_char,
            remote_url: *const c_char,
            error_out: *mut *mut c_char,
        ) -> *mut BedrockLldbSession;

        pub fn bedrock_lldb_command(
            session: *mut BedrockLldbSession,
            command: *const c_char,
            status_out: *mut c_int,
            succeeded_out: *mut c_int,
            output_out: *mut *mut c_char,
            error_out: *mut *mut c_char,
        ) -> c_int;

        pub fn bedrock_lldb_interrupt(
            session: *mut BedrockLldbSession,
            error_out: *mut *mut c_char,
        ) -> c_int;

        pub fn bedrock_lldb_detach(
            session: *mut BedrockLldbSession,
            error_out: *mut *mut c_char,
        ) -> c_int;

        pub fn bedrock_lldb_process_state(session: *mut BedrockLldbSession) -> c_int;

        pub fn bedrock_lldb_destroy(session: *mut BedrockLldbSession);

        pub fn bedrock_lldb_string_free(value: *mut c_char);
    }
}

#[cfg(test)]
mod tests {
    use super::{LldbConfig, LldbEvent, LldbSession, ProcessState, expand_command};
    use bedrock_debug::Debugger;
    use bedrock_machine::{ElfLoadOptions, Machine};
    use bedrock_toolchain::{
        BEDROCK_LLVM_BIN_ENV, BEDROCK_LLVM_ROOT_ENV, LinkOptions, LlvmToolchain,
    };
    use std::env;
    use std::fs;
    use std::net::TcpListener;
    use std::path::{Path, PathBuf};
    use std::sync::atomic::{AtomicU64, Ordering};
    use std::thread;
    use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};

    const PROGRAM: &str = r#"
    .text
    .globl _start
_start:
    NOP
    BKPT
"#;

    #[test]
    fn expands_bedrock_helper_commands_without_python() {
        assert_eq!(
            expand_command("br-pr 0x1000").unwrap(),
            vec![
                "process plugin packet monitor processor-reset 0x1000",
                "register write pc 0x1000"
            ]
        );
        assert_eq!(
            expand_command("br-reset 0x1000").unwrap(),
            vec![
                "process plugin packet monitor system-reset 0x1000",
                "register write pc 0x1000"
            ]
        );
        assert!(expand_command("br-pr").is_err());
    }

    #[test]
    fn lldb_attaches_to_bedrock_remote_and_runs_commands() {
        let Some(toolchain) = discover_toolchain() else {
            return;
        };

        let temp = TestTempDir::new("lldb-attach");
        let elf = assemble_and_link(&toolchain, temp.path(), PROGRAM);
        let bytes = fs::read(&elf).unwrap_or_else(|err| panic!("failed to read {elf:?}: {err}"));

        let mut machine = Machine::new();
        machine
            .load_elf(&bytes, ElfLoadOptions::default())
            .expect("LLVM-linked ELF should load");
        let mut debugger = Debugger::default();
        let listener = TcpListener::bind(("127.0.0.1", 0)).unwrap();
        let addr = listener.local_addr().unwrap().to_string();
        let remote = thread::spawn(move || {
            bedrock_debug_remote::run_tcp_listener(listener, &mut machine, &mut debugger)
        });

        let session = LldbSession::spawn(LldbConfig {
            elf_path: Some(elf),
            remote_addr: addr,
        })
        .expect("LLDB session should spawn");

        wait_for_connected(&session);
        session
            .send_command("register read pc")
            .expect("command should send");
        let result = wait_for_command(&session, "register read pc");
        assert!(result.output.contains("0x0000000000001000"), "{result:?}");

        session
            .send_command("br-pr 0x1000")
            .expect("br-pr should send");
        let result = wait_for_command(&session, "br-pr 0x1000");
        assert!(result.succeeded, "{result:?}");

        session
            .send_command("thread step-inst")
            .expect("step command should send");
        let result = wait_for_command(&session, "thread step-inst");
        assert!(result.succeeded, "{result:?}");

        session.detach().expect("detach should send");
        wait_for_exit(&session);
        remote
            .join()
            .expect("remote thread should join")
            .expect("remote session should finish");
    }

    fn wait_for_connected(session: &LldbSession) {
        let deadline = Instant::now() + Duration::from_secs(10);
        loop {
            match session.try_event() {
                Some(LldbEvent::Connected { .. }) => return,
                Some(LldbEvent::Exited { result }) => {
                    panic!("LLDB exited before connect: {result:?}")
                }
                Some(_) | None => {}
            }
            assert!(
                Instant::now() < deadline,
                "timed out waiting for LLDB connect"
            );
            thread::sleep(Duration::from_millis(10));
        }
    }

    fn wait_for_command(session: &LldbSession, command: &str) -> super::CommandResult {
        let deadline = Instant::now() + Duration::from_secs(10);
        loop {
            match session.try_event() {
                Some(LldbEvent::CommandResult(result)) if result.command == command => {
                    return result;
                }
                Some(LldbEvent::Exited { result }) => {
                    panic!("LLDB exited before command result: {result:?}");
                }
                Some(LldbEvent::ProcessState(ProcessState::Crashed)) => {
                    panic!("LLDB process crashed");
                }
                Some(_) | None => {}
            }
            assert!(
                Instant::now() < deadline,
                "timed out waiting for command {command}"
            );
            thread::sleep(Duration::from_millis(10));
        }
    }

    fn wait_for_exit(session: &LldbSession) {
        let deadline = Instant::now() + Duration::from_secs(10);
        loop {
            if let Some(LldbEvent::Exited { result }) = session.try_event() {
                assert!(result.is_ok(), "{result:?}");
                return;
            }
            assert!(Instant::now() < deadline, "timed out waiting for LLDB exit");
            thread::sleep(Duration::from_millis(10));
        }
    }

    fn discover_toolchain() -> Option<LlvmToolchain> {
        match LlvmToolchain::discover() {
            Ok(toolchain) => Some(toolchain),
            Err(err)
                if env::var_os(BEDROCK_LLVM_BIN_ENV).is_none()
                    && env::var_os(BEDROCK_LLVM_ROOT_ENV).is_none() =>
            {
                eprintln!(
                    "skipping LLDB integration test: set {BEDROCK_LLVM_ROOT_ENV} to the LLVM build directory; it is required for LLDB headers and libraries. {BEDROCK_LLVM_BIN_ENV} may override executable lookup only: {err}"
                );
                None
            }
            Err(err) => panic!("failed to load LLVM Bedrock toolchain: {err}"),
        }
    }

    fn assemble_and_link(toolchain: &LlvmToolchain, dir: &Path, source: &str) -> PathBuf {
        let asm = dir.join("program.s");
        let obj = dir.join("program.o");
        let elf = dir.join("program.elf");

        fs::write(&asm, source).unwrap_or_else(|err| panic!("failed to write {asm:?}: {err}"));
        toolchain
            .assemble_object(&asm, &obj)
            .expect("LLVM assembly should succeed");
        toolchain
            .link_executable(&obj, &elf, LinkOptions::default())
            .expect("LLD link should succeed");

        elf
    }

    struct TestTempDir {
        path: PathBuf,
    }

    impl TestTempDir {
        fn new(name: &str) -> Self {
            static COUNTER: AtomicU64 = AtomicU64::new(0);

            let nonce = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .expect("system clock should be after Unix epoch")
                .as_nanos();
            let counter = COUNTER.fetch_add(1, Ordering::Relaxed);
            let path = env::temp_dir().join(format!(
                "bedrock-lldb-{name}-{}-{nonce}-{counter}",
                std::process::id()
            ));
            fs::create_dir_all(&path)
                .unwrap_or_else(|err| panic!("failed to create {path:?}: {err}"));

            Self { path }
        }

        fn path(&self) -> &Path {
            &self.path
        }
    }

    impl Drop for TestTempDir {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.path);
        }
    }
}
