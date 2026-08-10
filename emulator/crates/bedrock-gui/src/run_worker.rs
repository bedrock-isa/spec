use bedrock_core::CpuState;
use bedrock_debug::{Debugger, StepResult};
use bedrock_devices::FramebufferDevice;
use bedrock_machine::Machine;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::mpsc::{self, Receiver, Sender, TryRecvError};
use std::thread;

const UNLIMITED_CONTROL_POLL_STEPS: u64 = 64;
const UNLIMITED_STEP_BUDGET: u64 = 0;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum FrameStepBudget {
    Limited(u64),
    Unlimited,
}

impl FrameStepBudget {
    pub(crate) fn limited(value: u64) -> Self {
        Self::Limited(value.max(1))
    }

    fn encode(self) -> u64 {
        match self {
            Self::Limited(value) => value.max(1),
            Self::Unlimited => UNLIMITED_STEP_BUDGET,
        }
    }

    fn decode(value: u64) -> Self {
        if value == UNLIMITED_STEP_BUDGET {
            Self::Unlimited
        } else {
            Self::Limited(value)
        }
    }
}

#[derive(Debug)]
pub(crate) struct ExecutionWorker {
    command_sender: Sender<ExecutionCommand>,
    event_receiver: Receiver<ExecutionEvent>,
    step_budget: Arc<AtomicU64>,
    frame_steps_remaining: Arc<AtomicU64>,
    snapshot_requested: Arc<AtomicBool>,
    worker_thread: thread::Thread,
}

impl ExecutionWorker {
    pub(crate) fn spawn(
        machine: Machine,
        debugger: Debugger,
        total_steps: u64,
        step_budget: FrameStepBudget,
    ) -> Result<Self, std::io::Error> {
        let (command_sender, command_receiver) = mpsc::channel();
        let (event_sender, event_receiver) = mpsc::channel();
        let step_budget = Arc::new(AtomicU64::new(step_budget.encode()));
        let worker_step_budget = Arc::clone(&step_budget);
        let frame_steps_remaining = Arc::new(AtomicU64::new(0));
        let worker_frame_steps_remaining = Arc::clone(&frame_steps_remaining);
        let snapshot_requested = Arc::new(AtomicBool::new(false));
        let worker_snapshot_requested = Arc::clone(&snapshot_requested);

        let join_handle = thread::Builder::new()
            .name("bedrock-gui-execution".to_owned())
            .spawn(move || {
                run_execution_loop(
                    machine,
                    debugger,
                    total_steps,
                    worker_step_budget,
                    worker_frame_steps_remaining,
                    worker_snapshot_requested,
                    command_receiver,
                    event_sender,
                );
            })?;
        let worker_thread = join_handle.thread().clone();
        drop(join_handle);

        Ok(Self {
            command_sender,
            event_receiver,
            step_budget,
            frame_steps_remaining,
            snapshot_requested,
            worker_thread,
        })
    }

    pub(crate) fn set_step_budget(&self, step_budget: FrameStepBudget) {
        self.step_budget
            .store(step_budget.encode(), Ordering::Relaxed);
        self.worker_thread.unpark();
    }

    pub(crate) fn request_pause(&self) {
        let _ = self.command_sender.send(ExecutionCommand::Pause);
        self.worker_thread.unpark();
    }

    pub(crate) fn push_keyboard_event(&self, event: u32) {
        let _ = self
            .command_sender
            .send(ExecutionCommand::PushKeyboardEvent(event));
        self.worker_thread.unpark();
    }

    pub(crate) fn request_frame_tick(&self) {
        match FrameStepBudget::decode(self.step_budget.load(Ordering::Acquire)) {
            FrameStepBudget::Limited(limit) => {
                if self
                    .frame_steps_remaining
                    .compare_exchange(0, limit, Ordering::AcqRel, Ordering::Acquire)
                    .is_ok()
                {
                    self.worker_thread.unpark();
                }
            }
            FrameStepBudget::Unlimited => {
                self.snapshot_requested.store(true, Ordering::Release);
                self.worker_thread.unpark();
            }
        }
    }

    pub(crate) fn try_event(&self) -> Option<ExecutionEvent> {
        self.event_receiver.try_recv().ok()
    }
}

impl Drop for ExecutionWorker {
    fn drop(&mut self) {
        let _ = self.command_sender.send(ExecutionCommand::Pause);
        self.worker_thread.unpark();
    }
}

#[derive(Debug)]
enum ExecutionCommand {
    Pause,
    PushKeyboardEvent(u32),
}

#[derive(Debug)]
pub(crate) enum ExecutionEvent {
    Snapshot(ExecutionSnapshot),
    Stopped {
        snapshot: ExecutionSnapshot,
        reason: ExecutionStopReason,
    },
}

#[derive(Debug, Clone)]
pub(crate) struct ExecutionSnapshot {
    pub machine: Option<Machine>,
    pub state: CpuState,
    pub framebuffer: FramebufferDevice,
    pub debugger: Debugger,
    pub total_steps: u64,
    pub last_result: Option<StepResult>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ExecutionStopReason {
    Paused,
    StepResult,
}

#[allow(clippy::too_many_arguments)]
fn run_execution_loop(
    mut machine: Machine,
    debugger: Debugger,
    mut total_steps: u64,
    step_budget: Arc<AtomicU64>,
    frame_steps_remaining: Arc<AtomicU64>,
    snapshot_requested: Arc<AtomicBool>,
    command_receiver: Receiver<ExecutionCommand>,
    event_sender: Sender<ExecutionEvent>,
) {
    let mut last_result = None;
    loop {
        match FrameStepBudget::decode(step_budget.load(Ordering::Relaxed)) {
            FrameStepBudget::Limited(_) => loop {
                if !matches!(
                    FrameStepBudget::decode(step_budget.load(Ordering::Acquire)),
                    FrameStepBudget::Limited(_)
                ) {
                    break;
                }

                if drain_commands(&mut machine, &command_receiver).pause {
                    send_stopped(
                        &event_sender,
                        machine,
                        debugger,
                        total_steps,
                        last_result,
                        ExecutionStopReason::Paused,
                    );
                    return;
                }

                let credit = match take_frame_step_credit(&frame_steps_remaining) {
                    Some(credit) => credit,
                    None => {
                        thread::park();
                        continue;
                    }
                };

                if matches!(
                    run_steps(
                        &mut machine,
                        &debugger,
                        &mut total_steps,
                        &mut last_result,
                        1,
                    ),
                    StepRunOutcome::Stopped
                ) {
                    send_stopped(
                        &event_sender,
                        machine,
                        debugger,
                        total_steps,
                        last_result,
                        ExecutionStopReason::StepResult,
                    );
                    return;
                }

                if credit == FrameStepCredit::Last {
                    send_snapshot(
                        &event_sender,
                        &machine,
                        &debugger,
                        total_steps,
                        last_result.clone(),
                    );
                }
            },
            FrameStepBudget::Unlimited => loop {
                if snapshot_requested.swap(false, Ordering::AcqRel) {
                    send_snapshot(
                        &event_sender,
                        &machine,
                        &debugger,
                        total_steps,
                        last_result.clone(),
                    );
                }

                if drain_commands(&mut machine, &command_receiver).pause {
                    send_stopped(
                        &event_sender,
                        machine,
                        debugger,
                        total_steps,
                        last_result,
                        ExecutionStopReason::Paused,
                    );
                    return;
                }
                if !matches!(
                    FrameStepBudget::decode(step_budget.load(Ordering::Relaxed)),
                    FrameStepBudget::Unlimited
                ) {
                    break;
                }
                if matches!(
                    run_steps(
                        &mut machine,
                        &debugger,
                        &mut total_steps,
                        &mut last_result,
                        UNLIMITED_CONTROL_POLL_STEPS,
                    ),
                    StepRunOutcome::Stopped
                ) {
                    send_stopped(
                        &event_sender,
                        machine,
                        debugger,
                        total_steps,
                        last_result,
                        ExecutionStopReason::StepResult,
                    );
                    return;
                }
            },
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum FrameStepCredit {
    More,
    Last,
}

fn take_frame_step_credit(frame_steps_remaining: &AtomicU64) -> Option<FrameStepCredit> {
    loop {
        let current = frame_steps_remaining.load(Ordering::Acquire);
        if current == 0 {
            return None;
        }

        match frame_steps_remaining.compare_exchange(
            current,
            current - 1,
            Ordering::AcqRel,
            Ordering::Acquire,
        ) {
            Ok(1) => return Some(FrameStepCredit::Last),
            Ok(_) => return Some(FrameStepCredit::More),
            Err(_) => continue,
        }
    }
}

#[derive(Debug, Clone, Copy, Default)]
struct ControlSignals {
    pause: bool,
}

fn drain_commands(
    machine: &mut Machine,
    command_receiver: &Receiver<ExecutionCommand>,
) -> ControlSignals {
    let mut signals = ControlSignals::default();
    loop {
        match command_receiver.try_recv() {
            Ok(command) => {
                signals |= apply_command(machine, command);
            }
            Err(TryRecvError::Empty) => return signals,
            Err(TryRecvError::Disconnected) => {
                signals.pause = true;
                return signals;
            }
        }
    }
}

fn apply_command(machine: &mut Machine, command: ExecutionCommand) -> ControlSignals {
    match command {
        ExecutionCommand::Pause => ControlSignals { pause: true },
        ExecutionCommand::PushKeyboardEvent(event) => {
            machine.board_mut().keyboard_mut().push_event(event);
            ControlSignals::default()
        }
    }
}

impl std::ops::BitOrAssign for ControlSignals {
    fn bitor_assign(&mut self, rhs: Self) {
        self.pause |= rhs.pause;
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum StepRunOutcome {
    Running { steps: u64 },
    Stopped,
}

fn run_steps(
    machine: &mut Machine,
    debugger: &Debugger,
    total_steps: &mut u64,
    last_result: &mut Option<StepResult>,
    steps: u64,
) -> StepRunOutcome {
    let mut completed = 0;
    for _ in 0..steps {
        let result = debugger.run_step(machine);
        *total_steps = total_steps.saturating_add(1);
        *last_result = Some(result.clone());
        completed += 1;

        if !matches!(result, StepResult::Running) {
            return StepRunOutcome::Stopped;
        }
    }
    StepRunOutcome::Running { steps: completed }
}

fn send_snapshot(
    event_sender: &Sender<ExecutionEvent>,
    machine: &Machine,
    debugger: &Debugger,
    total_steps: u64,
    last_result: Option<StepResult>,
) {
    let _ = event_sender.send(ExecutionEvent::Snapshot(light_snapshot(
        machine,
        debugger,
        total_steps,
        last_result,
    )));
}

fn send_stopped(
    event_sender: &Sender<ExecutionEvent>,
    machine: Machine,
    debugger: Debugger,
    total_steps: u64,
    last_result: Option<StepResult>,
    reason: ExecutionStopReason,
) {
    let _ = event_sender.send(ExecutionEvent::Stopped {
        snapshot: full_snapshot(machine, debugger, total_steps, last_result),
        reason,
    });
}

fn light_snapshot(
    machine: &Machine,
    debugger: &Debugger,
    total_steps: u64,
    last_result: Option<StepResult>,
) -> ExecutionSnapshot {
    ExecutionSnapshot {
        machine: None,
        state: machine.state().clone(),
        framebuffer: machine.board().framebuffer().clone(),
        debugger: debugger.clone(),
        total_steps,
        last_result,
    }
}

fn full_snapshot(
    machine: Machine,
    debugger: Debugger,
    total_steps: u64,
    last_result: Option<StepResult>,
) -> ExecutionSnapshot {
    let state = machine.state().clone();
    let framebuffer = machine.board().framebuffer().clone();
    ExecutionSnapshot {
        machine: Some(machine),
        state,
        framebuffer,
        debugger,
        total_steps,
        last_result,
    }
}

#[cfg(test)]
mod tests {
    use super::{ExecutionEvent, ExecutionStopReason, ExecutionWorker, FrameStepBudget};
    use bedrock_debug::{Debugger, StepResult};
    use bedrock_machine::Machine;
    use std::time::{Duration, Instant};

    #[test]
    fn worker_runs_machine_off_thread_and_reports_stop_result() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0xa0, 0x49]).unwrap();
        machine.processor_reset(0);

        let worker =
            ExecutionWorker::spawn(machine, Debugger::default(), 0, FrameStepBudget::limited(1))
                .unwrap();
        worker.request_frame_tick();
        let deadline = Instant::now() + Duration::from_secs(2);

        loop {
            if let Some(ExecutionEvent::Stopped { snapshot, reason }) = worker.try_event() {
                assert_eq!(reason, ExecutionStopReason::StepResult);
                assert_eq!(snapshot.last_result, Some(StepResult::Halted));
                assert_eq!(snapshot.total_steps, 1);
                return;
            }
            assert!(Instant::now() < deadline, "worker did not stop in time");
            std::thread::sleep(Duration::from_millis(1));
        }
    }

    #[test]
    fn unlimited_budget_has_no_finite_step_cap() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0xa0, 0x49]).unwrap();
        machine.processor_reset(0);

        let worker =
            ExecutionWorker::spawn(machine, Debugger::default(), 0, FrameStepBudget::Unlimited)
                .unwrap();
        let deadline = Instant::now() + Duration::from_secs(2);

        loop {
            if let Some(ExecutionEvent::Stopped { snapshot, reason }) = worker.try_event() {
                assert_eq!(reason, ExecutionStopReason::StepResult);
                assert_eq!(snapshot.last_result, Some(StepResult::Halted));
                assert_eq!(snapshot.total_steps, 1);
                return;
            }
            assert!(Instant::now() < deadline, "worker did not stop in time");
            std::thread::sleep(Duration::from_millis(1));
        }
    }

    #[test]
    #[ignore]
    fn profile_sync_vs_worker_step_throughput() {
        const STEPS: u64 = 200_000;

        let mut machine = nop_machine(STEPS);
        let started = Instant::now();
        for _ in 0..STEPS {
            assert_eq!(machine.step(), StepResult::Running);
        }
        let machine_step_elapsed = started.elapsed();

        let mut machine = nop_machine(STEPS);
        let debugger = Debugger::default();
        let started = Instant::now();
        for _ in 0..STEPS {
            assert_eq!(debugger.run_step(&mut machine), StepResult::Running);
        }
        let run_step_elapsed = started.elapsed();

        let worker = ExecutionWorker::spawn(
            nop_machine(STEPS),
            Debugger::default(),
            0,
            FrameStepBudget::limited(STEPS),
        )
        .unwrap();
        let started = Instant::now();
        worker.request_frame_tick();
        let snapshot = loop {
            if let Some(ExecutionEvent::Snapshot(snapshot)) = worker.try_event() {
                break snapshot;
            }
            assert!(
                started.elapsed() < Duration::from_secs(10),
                "worker snapshot timed out"
            );
            std::thread::yield_now();
        };
        let worker_elapsed = started.elapsed();
        assert_eq!(snapshot.total_steps, STEPS);

        eprintln!("profile steps={STEPS}");
        eprintln!(
            "machine.step           {:?} ({:.0} steps/s)",
            machine_step_elapsed,
            STEPS as f64 / machine_step_elapsed.as_secs_f64()
        );
        eprintln!(
            "debugger.run_step      {:?} ({:.0} steps/s)",
            run_step_elapsed,
            STEPS as f64 / run_step_elapsed.as_secs_f64()
        );
        eprintln!(
            "worker limited snapshot {:?} ({:.0} steps/s)",
            worker_elapsed,
            STEPS as f64 / worker_elapsed.as_secs_f64()
        );
        eprintln!(
            "worker/run_step ratio  {:.2}x",
            worker_elapsed.as_secs_f64() / run_step_elapsed.as_secs_f64()
        );

        let worker = ExecutionWorker::spawn(
            nop_machine(STEPS + 1024),
            Debugger::default(),
            0,
            FrameStepBudget::limited(256),
        )
        .unwrap();
        let started = Instant::now();
        let mut total_steps = 0;
        while total_steps < STEPS {
            worker.request_frame_tick();
            let snapshot = loop {
                if let Some(event) = worker.try_event() {
                    match event {
                        ExecutionEvent::Snapshot(snapshot) => break snapshot,
                        ExecutionEvent::Stopped { snapshot, reason } => {
                            panic!(
                                "worker stopped during profile at {} steps with {:?} / {:?}",
                                snapshot.total_steps, reason, snapshot.last_result
                            );
                        }
                    }
                }
                assert!(
                    started.elapsed() < Duration::from_secs(10),
                    "worker 256-step snapshot timed out"
                );
                std::thread::yield_now();
            };
            total_steps = snapshot.total_steps;
        }
        let worker_frequent_snapshot_elapsed = started.elapsed();
        eprintln!(
            "worker 256-step snapshots {:?} ({:.0} steps/s)",
            worker_frequent_snapshot_elapsed,
            total_steps as f64 / worker_frequent_snapshot_elapsed.as_secs_f64()
        );
        eprintln!(
            "worker 256/run_step ratio {:.2}x",
            worker_frequent_snapshot_elapsed.as_secs_f64() / run_step_elapsed.as_secs_f64()
        );
    }

    fn nop_machine(steps: u64) -> Machine {
        let mut machine = Machine::new();
        let program = vec![0x01; steps as usize];
        machine.load_program(0, &program).unwrap();
        machine.processor_reset(0);
        machine
    }
}
