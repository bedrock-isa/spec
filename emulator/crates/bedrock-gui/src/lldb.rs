use bedrock_debug::Debugger;
use bedrock_debug_remote::{HostControl, RemoteSessionConfig, ResetImage};
use bedrock_lldb::{LldbConfig, LldbError, LldbEvent};
use bedrock_machine::Machine;
use std::fmt;
use std::net::TcpListener;
use std::path::{Path, PathBuf};
use std::sync::mpsc::{self, Receiver, Sender};
use std::thread;

#[derive(Debug)]
pub(crate) struct LldbSession {
    addr: String,
    client: bedrock_lldb::LldbSession,
    host_control_sender: Sender<HostControl>,
    cancel_sender: Sender<()>,
    receiver: Receiver<LldbSessionOutcome>,
    snapshot_receiver: Receiver<LldbSessionSnapshot>,
}

impl LldbSession {
    pub(crate) fn addr(&self) -> &str {
        &self.addr
    }

    pub(crate) fn send_command(&self, command: impl Into<String>) -> Result<(), LldbError> {
        self.client.send_command(command)
    }

    pub(crate) fn interrupt(&self) -> Result<(), LldbError> {
        let _ = self.host_control_sender.send(HostControl::Interrupt);
        self.client.interrupt()
    }

    pub(crate) fn detach(&self) -> Result<(), LldbError> {
        self.client.detach()
    }

    pub(crate) fn push_keyboard_event(&self, event: u32) {
        let _ = self
            .host_control_sender
            .send(HostControl::PushKeyboardEvent(event));
    }

    pub(crate) fn cancel_waiting_listener(&self) {
        let _ = self.cancel_sender.send(());
    }

    pub(crate) fn try_lldb_event(&self) -> Option<LldbEvent> {
        self.client.try_event()
    }

    pub(crate) fn try_finish(&self) -> Option<LldbSessionOutcome> {
        self.receiver.try_recv().ok()
    }

    pub(crate) fn try_snapshot(&self) -> Option<LldbSessionSnapshot> {
        self.snapshot_receiver.try_recv().ok()
    }
}

#[derive(Debug)]
pub(crate) struct LldbSessionOutcome {
    pub machine: Machine,
    pub debugger: Debugger,
    pub result: Result<(), String>,
}

#[derive(Debug, Clone)]
pub(crate) struct LldbSessionSnapshot {
    pub machine: Machine,
    pub debugger: Debugger,
}

#[derive(Debug)]
pub(crate) enum LldbLaunchError {
    Io(std::io::Error),
    Lldb(LldbError),
}

impl fmt::Display for LldbLaunchError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(error) => write!(f, "{error}"),
            Self::Lldb(error) => write!(f, "{error}"),
        }
    }
}

impl From<std::io::Error> for LldbLaunchError {
    fn from(error: std::io::Error) -> Self {
        Self::Io(error)
    }
}

impl From<LldbError> for LldbLaunchError {
    fn from(error: LldbError) -> Self {
        Self::Lldb(error)
    }
}

pub(crate) fn launch_lldb_session(
    machine: Machine,
    debugger: Debugger,
    elf_path: Option<&Path>,
    reset_image: Option<ResetImage>,
) -> Result<LldbSession, LldbLaunchError> {
    let listener = TcpListener::bind(("127.0.0.1", 0))?;
    let addr = listener.local_addr()?.to_string();

    let (sender, receiver) = mpsc::channel();
    let (snapshot_sender, snapshot_receiver) = mpsc::channel();
    let (host_control_sender, host_control_receiver) = mpsc::channel();
    let (cancel_sender, cancel_receiver) = mpsc::channel();
    let thread_addr = addr.clone();
    thread::Builder::new()
        .name("bedrock-lldb-remote".to_owned())
        .spawn(move || {
            let mut machine = machine;
            let mut debugger = debugger;
            let result = bedrock_debug_remote::run_tcp_listener_configured_with_observer_until(
                listener,
                &mut machine,
                &mut debugger,
                RemoteSessionConfig { reset_image },
                Some(host_control_receiver),
                move |machine: &Machine, debugger: &Debugger| {
                    let _ = snapshot_sender.send(LldbSessionSnapshot {
                        machine: machine.clone(),
                        debugger: debugger.clone(),
                    });
                },
                || cancel_receiver.try_recv().is_ok(),
            )
            .map_err(|error| error.to_string());
            let _ = sender.send(LldbSessionOutcome {
                machine,
                debugger,
                result,
            });
            tracing::info!(addr = %thread_addr, "liblldb remote session ended");
        })?;

    let client = match bedrock_lldb::LldbSession::spawn(LldbConfig {
        elf_path: elf_path.map(PathBuf::from),
        remote_addr: addr.clone(),
    }) {
        Ok(client) => client,
        Err(error) => {
            let _ = cancel_sender.send(());
            return Err(error.into());
        }
    };

    Ok(LldbSession {
        addr,
        client,
        host_control_sender,
        cancel_sender,
        receiver,
        snapshot_receiver,
    })
}
