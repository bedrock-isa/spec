use crate::panels::{self, controls::ControlActions};
use crate::parse::parse_u64;
use crate::run_worker::{ExecutionEvent, ExecutionSnapshot, ExecutionStopReason, ExecutionWorker};
use bedrock_debug::{Debugger, StepResult};
use bedrock_debug_remote::ResetImage;
use bedrock_lldb::{CommandResult, LldbEvent, ProcessState};
use bedrock_machine::{ElfLoadOptions, ElfLoadResult, Machine};
use std::path::PathBuf;
use std::time::{Duration, Instant};

const DEFAULT_STEPS_PER_FRAME: u64 = 256;
const DEFAULT_LLDB_CONSOLE_HEIGHT: f32 = 240.0;
const MIN_LLDB_CONSOLE_HEIGHT: f32 = 120.0;
const MAX_LLDB_CONSOLE_HEIGHT: f32 = 520.0;
const MIN_MAIN_WORKSPACE_HEIGHT: f32 = 120.0;
const LLDB_SPLITTER_HEIGHT: f32 = 7.0;
const PERF_SAMPLE_WINDOW: Duration = Duration::from_secs(1);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ActiveView {
    Display,
    Trace,
}

impl ActiveView {
    const ALL: [Self; 2] = [Self::Display, Self::Trace];

    fn label(self) -> &'static str {
        match self {
            Self::Display => "Display",
            Self::Trace => "Trace",
        }
    }
}

#[derive(Debug, Clone)]
pub(crate) struct LoadedElf {
    pub path: PathBuf,
    pub result: ElfLoadResult,
}

pub struct BedrockGuiApp {
    machine: Machine,
    debugger: Debugger,
    controls: panels::controls::ControlPanelState,
    framebuffer: panels::framebuffer::FramebufferPanelState,
    memory: panels::memory::MemoryPanelState,
    disassembly: panels::disasm::DisassemblyPanelState,
    lldb_panel: panels::lldb::LldbPanelState,
    lldb_console_height: f32,
    active_view: ActiveView,
    loaded_elf: Option<LoadedElf>,
    running: bool,
    total_steps: u64,
    last_result: Option<StepResult>,
    status: String,
    perf: PerfStats,
    lldb_session: Option<crate::lldb::LldbSession>,
    execution_worker: Option<ExecutionWorker>,
}

#[derive(Debug)]
struct PerfStats {
    window_start: Instant,
    steps_start: u64,
    frames: u64,
    snapshots: u64,
    update_time: Duration,
    framebuffer_time: Duration,
    current: PerfSample,
}

impl Default for PerfStats {
    fn default() -> Self {
        Self {
            window_start: Instant::now(),
            steps_start: 0,
            frames: 0,
            snapshots: 0,
            update_time: Duration::ZERO,
            framebuffer_time: Duration::ZERO,
            current: PerfSample::default(),
        }
    }
}

impl PerfStats {
    fn record_frame(
        &mut self,
        total_steps: u64,
        snapshots: u64,
        update_elapsed: Duration,
        framebuffer_elapsed: Duration,
    ) {
        self.frames = self.frames.saturating_add(1);
        self.snapshots = self.snapshots.saturating_add(snapshots);
        self.update_time += update_elapsed;
        self.framebuffer_time += framebuffer_elapsed;

        let elapsed = self.window_start.elapsed();
        if elapsed < PERF_SAMPLE_WINDOW {
            return;
        }

        let seconds = elapsed.as_secs_f64();
        let frames = self.frames.max(1) as f64;
        self.current = PerfSample {
            frames_per_second: self.frames as f64 / seconds,
            steps_per_second: total_steps.saturating_sub(self.steps_start) as f64 / seconds,
            snapshots_per_second: self.snapshots as f64 / seconds,
            average_update_ms: self.update_time.as_secs_f64() * 1000.0 / frames,
            average_framebuffer_ms: self.framebuffer_time.as_secs_f64() * 1000.0 / frames,
        };

        self.window_start = Instant::now();
        self.steps_start = total_steps;
        self.frames = 0;
        self.snapshots = 0;
        self.update_time = Duration::ZERO;
        self.framebuffer_time = Duration::ZERO;
    }

    fn summary(&self) -> String {
        format!(
            "perf {:.0} fps  {:.0} step/s  {:.0} snap/s  update {:.2}ms  fb {:.2}ms",
            self.current.frames_per_second,
            self.current.steps_per_second,
            self.current.snapshots_per_second,
            self.current.average_update_ms,
            self.current.average_framebuffer_ms
        )
    }
}

#[derive(Debug, Clone, Copy, Default)]
struct PerfSample {
    frames_per_second: f64,
    steps_per_second: f64,
    snapshots_per_second: f64,
    average_update_ms: f64,
    average_framebuffer_ms: f64,
}

#[derive(Debug, Clone, Copy, Default)]
struct PollSummary {
    changed: bool,
    snapshots: u64,
}

struct CentralWorkspaceResult {
    lldb_actions: panels::lldb::LldbPanelActions,
    framebuffer_elapsed: Duration,
}

impl Default for BedrockGuiApp {
    fn default() -> Self {
        Self {
            machine: Machine::new(),
            debugger: Debugger::default(),
            controls: panels::controls::ControlPanelState {
                steps_per_frame: DEFAULT_STEPS_PER_FRAME,
                ..Default::default()
            },
            framebuffer: panels::framebuffer::FramebufferPanelState::default(),
            memory: panels::memory::MemoryPanelState::default(),
            disassembly: panels::disasm::DisassemblyPanelState::default(),
            lldb_panel: panels::lldb::LldbPanelState::default(),
            lldb_console_height: DEFAULT_LLDB_CONSOLE_HEIGHT,
            active_view: ActiveView::Display,
            loaded_elf: None,
            running: false,
            total_steps: 0,
            last_result: None,
            status: "Processor reset at 0x0000000000000000".to_owned(),
            perf: PerfStats::default(),
            lldb_session: None,
            execution_worker: None,
        }
    }
}

impl eframe::App for BedrockGuiApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        let update_started = Instant::now();
        let lldb_poll = self.poll_lldb_session();
        if lldb_poll.changed {
            ctx.request_repaint();
        }
        let execution_poll = self.poll_execution_worker();
        if execution_poll.changed {
            ctx.request_repaint();
        }

        let perf_summary = self.perf.summary();
        let actions = egui::TopBottomPanel::top("controls")
            .resizable(false)
            .show(ctx, |ui| {
                panels::controls::show(
                    ui,
                    &mut self.controls,
                    self.running,
                    self.total_steps,
                    self.last_result.as_ref(),
                    self.debugger.breakpoints().all().len(),
                    self.lldb_session.is_some(),
                    &perf_summary,
                )
            })
            .inner;
        self.apply_control_actions(actions);

        egui::SidePanel::left("cpu")
            .resizable(true)
            .default_width(280.0)
            .show(ctx, |ui| {
                egui::ScrollArea::vertical()
                    .id_salt("cpu_sidebar_scroll")
                    .auto_shrink([false, false])
                    .show(ui, |ui| {
                        panels::cpu::show(
                            ui,
                            &self.machine,
                            &mut self.debugger,
                            self.lldb_session.is_none() && self.execution_worker.is_none(),
                        );
                        ui.separator();
                        ui.heading("Target");
                        if let Some(loaded) = &self.loaded_elf {
                            ui.label(loaded.path.display().to_string());
                            ui.monospace(format!("entry 0x{:016x}", loaded.result.entry));
                            ui.monospace(format!("segments {}", loaded.result.segments.len()));
                        } else {
                            ui.label("No ELF loaded");
                        }
                        if let Some(session) = &self.lldb_session {
                            ui.separator();
                            ui.heading("LLDB");
                            ui.monospace(session.addr());
                            ui.label("internal console");
                        }
                        ui.separator();
                        ui.heading("Status");
                        ui.label(&self.status);
                    });
            });

        egui::SidePanel::right("debug_observers")
            .resizable(true)
            .default_width(440.0)
            .min_width(320.0)
            .max_width(760.0)
            .show(ctx, |ui| {
                let available_height = ui.available_height();
                let disassembly_height = (available_height * 0.55)
                    .max(96.0)
                    .min((available_height - 160.0).max(96.0));
                ui.allocate_ui_with_layout(
                    egui::vec2(ui.available_width(), disassembly_height),
                    egui::Layout::top_down(egui::Align::Min),
                    |ui| {
                        panels::disasm::show(
                            ui,
                            &mut self.disassembly,
                            &self.machine,
                            self.loaded_elf.as_ref(),
                        );
                    },
                );
                ui.separator();
                ui.allocate_ui_with_layout(
                    ui.available_size(),
                    egui::Layout::top_down(egui::Align::Min),
                    |ui| {
                        panels::memory::show(ui, &mut self.memory, &self.machine);
                    },
                );
            });

        let workspace = egui::CentralPanel::default()
            .show(ctx, |ui| self.show_central_workspace(ui, ctx))
            .inner;
        if workspace.lldb_actions.start {
            self.open_lldb_session();
        }
        if let Some(command) = workspace.lldb_actions.submit {
            self.send_lldb_command(command);
        }
        if workspace.lldb_actions.detach {
            self.detach_lldb();
        }

        self.capture_keyboard_input(ctx);

        if self.lldb_session.is_some() {
            ctx.request_repaint_after(Duration::from_millis(33));
        }
        if let Some(worker) = &self.execution_worker {
            worker.set_step_budget(self.controls.step_budget());
            worker.request_frame_tick();
            ctx.request_repaint();
        }

        self.perf.record_frame(
            self.total_steps,
            lldb_poll.snapshots + execution_poll.snapshots,
            update_started.elapsed(),
            workspace.framebuffer_elapsed,
        );
    }
}

impl BedrockGuiApp {
    fn show_central_workspace(
        &mut self,
        ui: &mut egui::Ui,
        ctx: &egui::Context,
    ) -> CentralWorkspaceResult {
        ui.horizontal_wrapped(|ui| {
            for view in ActiveView::ALL {
                ui.selectable_value(&mut self.active_view, view, view.label());
            }
        });
        ui.separator();

        self.show_lldb_split_workspace(ui, ctx)
    }

    fn show_lldb_split_workspace(
        &mut self,
        ui: &mut egui::Ui,
        ctx: &egui::Context,
    ) -> CentralWorkspaceResult {
        let available_height = ui.available_height();
        let max_lldb_height = (available_height - MIN_MAIN_WORKSPACE_HEIGHT - LLDB_SPLITTER_HEIGHT)
            .clamp(MIN_LLDB_CONSOLE_HEIGHT, MAX_LLDB_CONSOLE_HEIGHT)
            .min((available_height - LLDB_SPLITTER_HEIGHT).max(0.0));
        let min_lldb_height = MIN_LLDB_CONSOLE_HEIGHT.min(max_lldb_height);
        self.lldb_console_height = self
            .lldb_console_height
            .clamp(min_lldb_height, max_lldb_height);

        let main_height =
            (available_height - self.lldb_console_height - LLDB_SPLITTER_HEIGHT).max(0.0);
        let mut framebuffer_elapsed = Duration::ZERO;
        ui.allocate_ui_with_layout(
            egui::vec2(ui.available_width(), main_height),
            egui::Layout::top_down(egui::Align::Min),
            |ui| {
                framebuffer_elapsed += self.show_active_view(ui, ctx);
            },
        );

        let (splitter_rect, splitter_response) = ui.allocate_exact_size(
            egui::vec2(ui.available_width(), LLDB_SPLITTER_HEIGHT),
            egui::Sense::click_and_drag(),
        );
        if splitter_response.hovered() || splitter_response.dragged() {
            ctx.set_cursor_icon(egui::CursorIcon::ResizeVertical);
        }
        if splitter_response.dragged() {
            let delta_y = ui.input(|input| input.pointer.delta().y);
            self.lldb_console_height =
                (self.lldb_console_height - delta_y).clamp(min_lldb_height, max_lldb_height);
            ctx.request_repaint();
        }
        let stroke = if splitter_response.dragged() {
            ui.visuals().widgets.active.fg_stroke
        } else if splitter_response.hovered() {
            ui.visuals().widgets.hovered.fg_stroke
        } else {
            ui.visuals().widgets.noninteractive.bg_stroke
        };
        ui.painter()
            .hline(splitter_rect.x_range(), splitter_rect.center().y, stroke);

        let lldb_actions = ui
            .allocate_ui_with_layout(
                egui::vec2(ui.available_width(), self.lldb_console_height),
                egui::Layout::top_down(egui::Align::Min),
                |ui| panels::lldb::show(ui, &mut self.lldb_panel, self.lldb_session.is_some()),
            )
            .inner;

        CentralWorkspaceResult {
            lldb_actions,
            framebuffer_elapsed,
        }
    }

    fn show_active_view(&mut self, ui: &mut egui::Ui, ctx: &egui::Context) -> Duration {
        match self.active_view {
            ActiveView::Display => {
                let started = Instant::now();
                panels::framebuffer::show(ui, ctx, &mut self.framebuffer, &self.machine);
                started.elapsed()
            }
            ActiveView::Trace => {
                panels::trace::show(ui, &self.debugger);
                Duration::ZERO
            }
        }
    }

    fn apply_control_actions(&mut self, actions: ControlActions) {
        if self.execution_worker.is_some() {
            if actions.toggle_running {
                self.pause_execution_worker();
            }
            return;
        }

        if self.lldb_session.is_some() {
            if actions.load_elf {
                self.status = "Detach LLDB before loading a different ELF".to_owned();
            }
            if actions.processor_reset {
                self.lldb_processor_reset();
            }
            if actions.system_reset {
                self.lldb_system_reset();
            }
            if actions.step {
                self.send_lldb_command("thread step-inst".to_owned());
            }
            if actions.toggle_running {
                self.toggle_lldb_running();
            }
            if actions.add_breakpoint {
                self.lldb_add_breakpoint();
            }
            if actions.remove_breakpoint {
                self.lldb_remove_breakpoint();
            }
            return;
        }

        if actions.load_elf {
            self.load_elf();
        }
        if actions.processor_reset {
            self.processor_reset();
        }
        if actions.system_reset {
            self.system_reset();
        }
        if actions.step {
            self.running = false;
            self.step_once();
        }
        if actions.toggle_running {
            self.start_execution_worker();
        }
        if actions.add_breakpoint {
            self.add_breakpoint();
        }
        if actions.remove_breakpoint {
            self.remove_breakpoint();
        }
    }

    fn poll_lldb_session(&mut self) -> PollSummary {
        let (latest_snapshot, snapshot_count, lldb_events, outcome) = {
            let Some(session) = self.lldb_session.as_ref() else {
                return PollSummary::default();
            };

            let mut latest_snapshot = None;
            let mut snapshot_count = 0;
            while let Some(snapshot) = session.try_snapshot() {
                latest_snapshot = Some(snapshot);
                snapshot_count += 1;
            }
            let mut lldb_events = Vec::new();
            while let Some(event) = session.try_lldb_event() {
                lldb_events.push(event);
            }
            let outcome = session.try_finish();
            if outcome.is_none()
                && lldb_events
                    .iter()
                    .any(|event| matches!(event, LldbEvent::Exited { .. }))
            {
                session.cancel_waiting_listener();
            }

            (latest_snapshot, snapshot_count, lldb_events, outcome)
        };

        let mut changed = false;
        if let Some(snapshot) = latest_snapshot {
            self.machine = snapshot.machine;
            self.debugger = snapshot.debugger;
            self.framebuffer.invalidate();
            self.last_result = self
                .debugger
                .trace()
                .back()
                .map(|event| event.result.clone());
            changed = true;
        }

        for event in lldb_events {
            self.handle_lldb_event(event);
            changed = true;
        }

        let Some(outcome) = outcome else {
            return PollSummary {
                changed,
                snapshots: snapshot_count,
            };
        };

        self.lldb_session = None;
        self.machine = outcome.machine;
        self.debugger = outcome.debugger;
        self.running = false;
        self.framebuffer.invalidate();
        self.last_result = self
            .debugger
            .trace()
            .back()
            .map(|event| event.result.clone());
        self.status = match outcome.result {
            Ok(()) => "LLDB session detached".to_owned(),
            Err(error) => format!("LLDB remote ended: {error}"),
        };
        self.lldb_panel.push_status(&self.status);
        PollSummary {
            changed: true,
            snapshots: snapshot_count,
        }
    }

    fn poll_execution_worker(&mut self) -> PollSummary {
        let events = {
            let Some(worker) = self.execution_worker.as_ref() else {
                return PollSummary::default();
            };

            let mut events = Vec::new();
            while let Some(event) = worker.try_event() {
                events.push(event);
            }
            events
        };

        if events.is_empty() {
            return PollSummary::default();
        };

        let mut snapshot_count = 0;
        let mut latest_snapshot = None;
        let mut stopped = None;
        for event in events {
            match event {
                ExecutionEvent::Snapshot(snapshot) => {
                    snapshot_count += 1;
                    latest_snapshot = Some(snapshot);
                }
                ExecutionEvent::Stopped { snapshot, reason } => {
                    snapshot_count += 1;
                    stopped = Some((snapshot, reason));
                }
            }
        }

        if let Some((snapshot, reason)) = stopped {
            self.apply_execution_snapshot(snapshot);
            self.execution_worker = None;
            self.running = false;
            self.status = match reason {
                ExecutionStopReason::Paused => "Paused".to_owned(),
                ExecutionStopReason::StepResult => self
                    .last_result
                    .as_ref()
                    .map_or_else(|| "Stopped".to_owned(), |result| format!("{result:?}")),
            };
            return PollSummary {
                changed: true,
                snapshots: snapshot_count,
            };
        };

        if let Some(snapshot) = latest_snapshot {
            self.apply_execution_snapshot(snapshot);
            return PollSummary {
                changed: true,
                snapshots: snapshot_count,
            };
        }

        PollSummary {
            changed: false,
            snapshots: snapshot_count,
        }
    }

    fn apply_execution_snapshot(&mut self, snapshot: ExecutionSnapshot) {
        if let Some(machine) = snapshot.machine {
            self.machine = machine;
        } else {
            *self.machine.cpu_mut().state_mut() = snapshot.state;
            *self.machine.board_mut().framebuffer_mut() = snapshot.framebuffer;
        }
        self.debugger = snapshot.debugger;
        self.total_steps = snapshot.total_steps;
        self.last_result = snapshot.last_result;
        self.framebuffer.invalidate();
    }

    fn load_elf(&mut self) {
        let path_text = self.controls.elf_path.trim();
        if path_text.is_empty() {
            self.status = "ELF path is empty".to_owned();
            return;
        }

        let load_base = match parse_u64(&self.controls.load_base) {
            Ok(load_base) => load_base,
            Err(error) => {
                self.status = format!("Invalid load base: {error}");
                return;
            }
        };

        let path = PathBuf::from(path_text);
        let bytes = match std::fs::read(&path) {
            Ok(bytes) => bytes,
            Err(error) => {
                self.status = format!("Failed to read ELF: {error}");
                return;
            }
        };

        let mut machine = Machine::new();
        let result = match machine.load_elf(&bytes, ElfLoadOptions { load_base }) {
            Ok(result) => result,
            Err(error) => {
                self.status = format!("Failed to load ELF: {error}");
                return;
            }
        };

        self.machine = machine;
        self.debugger = Debugger::default();
        self.framebuffer.invalidate();
        self.loaded_elf = Some(LoadedElf {
            path: path.clone(),
            result: result.clone(),
        });
        self.running = false;
        self.total_steps = 0;
        self.last_result = None;
        self.controls.reset_pc = format!("0x{:x}", result.entry);

        match self.disassembly.load_from_llvm(&path) {
            Ok(()) => {
                self.status = format!("Loaded {} at entry 0x{:016x}", path.display(), result.entry);
            }
            Err(error) => {
                self.status = format!(
                    "Loaded {} at entry 0x{:016x}; disassembly unavailable: {error}",
                    path.display(),
                    result.entry
                );
            }
        }
    }

    fn open_lldb_session(&mut self) {
        if self.execution_worker.is_some() {
            self.status = "Pause emulator before starting LLDB".to_owned();
            return;
        }
        self.running = false;
        let reset_image = match self.lldb_reset_image() {
            Ok(reset_image) => reset_image,
            Err(error) => {
                self.status = error;
                return;
            }
        };
        let elf_path = self.loaded_elf.as_ref().map(|loaded| loaded.path.as_path());
        match crate::lldb::launch_lldb_session(
            self.machine.clone(),
            self.debugger.clone(),
            elf_path,
            reset_image,
        ) {
            Ok(session) => {
                self.status = format!("LLDB connecting to {}", session.addr());
                self.lldb_panel.push_status(&self.status);
                self.lldb_session = Some(session);
            }
            Err(error) => {
                self.status = format!("Failed to start LLDB: {error}");
            }
        }
    }

    fn lldb_reset_image(&self) -> Result<Option<ResetImage>, String> {
        let Some(loaded) = &self.loaded_elf else {
            return Ok(None);
        };

        let load_base = parse_u64(&self.controls.load_base)
            .map_err(|error| format!("Invalid load base: {error}"))?;
        let bytes = std::fs::read(&loaded.path)
            .map_err(|error| format!("Failed to read ELF for LLDB reset image: {error}"))?;
        Ok(Some(ResetImage { bytes, load_base }))
    }

    fn processor_reset(&mut self) {
        match parse_u64(&self.controls.reset_pc) {
            Ok(pc) => {
                self.machine.processor_reset(pc);
                self.running = false;
                self.last_result = None;
                self.total_steps = 0;
                self.status = format!("Processor reset at 0x{pc:016x}");
            }
            Err(error) => {
                self.status = format!("Invalid reset PC: {error}");
            }
        }
    }

    fn system_reset(&mut self) {
        let pc = match parse_u64(&self.controls.reset_pc) {
            Ok(pc) => pc,
            Err(error) => {
                self.status = format!("Invalid reset PC: {error}");
                return;
            }
        };

        let Some(loaded) = self.loaded_elf.clone() else {
            self.machine.system_reset(pc);
            self.after_reset();
            self.status = format!("System reset at 0x{pc:016x}");
            return;
        };

        let bytes = match std::fs::read(&loaded.path) {
            Ok(bytes) => bytes,
            Err(error) => {
                self.status = format!("Failed to reload ELF for system reset: {error}");
                return;
            }
        };

        let load_base = match parse_u64(&self.controls.load_base) {
            Ok(load_base) => load_base,
            Err(error) => {
                self.status = format!("Invalid load base: {error}");
                return;
            }
        };

        let mut machine = Machine::new();
        let result = match machine.load_elf(&bytes, ElfLoadOptions { load_base }) {
            Ok(result) => result,
            Err(error) => {
                self.status = format!("Failed to reload ELF for system reset: {error}");
                return;
            }
        };

        self.machine = machine;
        self.loaded_elf = Some(LoadedElf {
            path: loaded.path.clone(),
            result: result.clone(),
        });
        self.controls.reset_pc = format!("0x{:x}", result.entry);
        self.after_reset();
        self.status = format!(
            "System reset and reloaded {} at entry 0x{:016x}",
            loaded.path.display(),
            result.entry
        );
    }

    fn after_reset(&mut self) {
        self.running = false;
        self.last_result = None;
        self.total_steps = 0;
        self.framebuffer.invalidate();
    }

    fn add_breakpoint(&mut self) {
        match parse_u64(&self.controls.breakpoint_addr) {
            Ok(addr) => {
                self.debugger.breakpoints_mut().add(addr);
                self.status = format!("Breakpoint added at 0x{addr:016x}");
            }
            Err(error) => {
                self.status = format!("Invalid breakpoint address: {error}");
            }
        }
    }

    fn remove_breakpoint(&mut self) {
        match parse_u64(&self.controls.breakpoint_addr) {
            Ok(addr) => {
                self.debugger.breakpoints_mut().remove(addr);
                self.status = format!("Breakpoint removed at 0x{addr:016x}");
            }
            Err(error) => {
                self.status = format!("Invalid breakpoint address: {error}");
            }
        }
    }

    fn step_once(&mut self) {
        let result = self.debugger.step(&mut self.machine);
        self.total_steps = self.total_steps.saturating_add(1);
        self.last_result = Some(result.clone());
        self.status = format!("{result:?}");
    }

    fn start_execution_worker(&mut self) {
        if self.lldb_session.is_some() {
            self.toggle_lldb_running();
            return;
        }
        if self.execution_worker.is_some() {
            self.pause_execution_worker();
            return;
        }

        match ExecutionWorker::spawn(
            self.machine.clone(),
            self.debugger.clone(),
            self.total_steps,
            self.controls.step_budget(),
        ) {
            Ok(worker) => {
                self.execution_worker = Some(worker);
                self.running = true;
                self.status = "Running".to_owned();
            }
            Err(error) => {
                self.status = format!("Failed to start execution worker: {error}");
            }
        }
    }

    fn pause_execution_worker(&mut self) {
        if let Some(worker) = &self.execution_worker {
            worker.request_pause();
            self.status = "Pause requested".to_owned();
        }
    }

    fn send_lldb_command(&mut self, command: String) {
        let Some(session) = self.lldb_session.as_ref() else {
            self.status = "LLDB is not active".to_owned();
            return;
        };

        self.lldb_panel.push_prompt(&command);
        match session.send_command(command) {
            Ok(()) => {
                self.status = "LLDB command sent".to_owned();
            }
            Err(error) => {
                self.status = format!("Failed to send LLDB command: {error}");
                self.lldb_panel.push_error(&self.status);
            }
        }
    }

    fn detach_lldb(&mut self) {
        let Some(session) = self.lldb_session.as_ref() else {
            return;
        };
        self.lldb_panel.push_prompt("detach");
        match session.detach() {
            Ok(()) => {
                self.status = "Detaching LLDB".to_owned();
            }
            Err(error) => {
                self.status = format!("Failed to detach LLDB: {error}");
                self.lldb_panel.push_error(&self.status);
            }
        }
    }

    fn toggle_lldb_running(&mut self) {
        if self.running {
            let Some(session) = self.lldb_session.as_ref() else {
                return;
            };
            self.lldb_panel.push_status("interrupt");
            match session.interrupt() {
                Ok(()) => {
                    self.status = "Interrupt requested".to_owned();
                    self.running = false;
                }
                Err(error) => {
                    self.status = format!("Failed to interrupt LLDB: {error}");
                    self.lldb_panel.push_error(&self.status);
                }
            }
        } else {
            self.running = true;
            self.send_lldb_command("continue".to_owned());
        }
    }

    fn lldb_processor_reset(&mut self) {
        match parse_u64(&self.controls.reset_pc) {
            Ok(pc) => self.send_lldb_command(format!("br-pr 0x{pc:x}")),
            Err(error) => {
                self.status = format!("Invalid reset PC: {error}");
            }
        }
    }

    fn lldb_system_reset(&mut self) {
        match parse_u64(&self.controls.reset_pc) {
            Ok(pc) => self.send_lldb_command(format!("br-reset 0x{pc:x}")),
            Err(error) => {
                self.status = format!("Invalid reset PC: {error}");
            }
        }
    }

    fn lldb_add_breakpoint(&mut self) {
        match parse_u64(&self.controls.breakpoint_addr) {
            Ok(addr) => self.send_lldb_command(format!(
                "process plugin packet monitor breakpoint-add 0x{addr:x}"
            )),
            Err(error) => {
                self.status = format!("Invalid breakpoint address: {error}");
            }
        }
    }

    fn lldb_remove_breakpoint(&mut self) {
        match parse_u64(&self.controls.breakpoint_addr) {
            Ok(addr) => self.send_lldb_command(format!(
                "process plugin packet monitor breakpoint-remove 0x{addr:x}"
            )),
            Err(error) => {
                self.status = format!("Invalid breakpoint address: {error}");
            }
        }
    }

    fn handle_lldb_event(&mut self, event: LldbEvent) {
        match event {
            LldbEvent::Connected { remote_addr } => {
                self.status = format!("LLDB connected to {remote_addr}");
                self.lldb_panel.push_status(&self.status);
            }
            LldbEvent::CommandResult(result) => self.handle_lldb_command_result(result),
            LldbEvent::ProcessState(state) => {
                self.running = matches!(state, ProcessState::Running | ProcessState::Stepping);
                self.lldb_panel
                    .set_process_state(format!("state {}", process_state_label(state)));
            }
            LldbEvent::Exited { result } => {
                self.running = false;
                self.status = match result {
                    Ok(()) => "LLDB client exited".to_owned(),
                    Err(error) => format!("LLDB client exited: {error}"),
                };
                self.lldb_panel.push_status(&self.status);
            }
        }
    }

    fn handle_lldb_command_result(&mut self, result: CommandResult) {
        if !result.output.is_empty() {
            self.lldb_panel.push_output(&result.output);
        }
        if !result.error.is_empty() {
            self.lldb_panel.push_error(&result.error);
        }
        self.status = if result.succeeded {
            format!("LLDB command completed: {}", result.command)
        } else {
            format!("LLDB command failed: {}", result.command)
        };
    }

    fn capture_keyboard_input(&mut self, ctx: &egui::Context) {
        if !self.machine_keyboard_accepts_input(ctx) {
            return;
        }

        let (events, modifiers) = ctx.input(|input| (input.events.clone(), input.modifiers));
        for encoded in encode_input_events(&events, modifiers) {
            self.push_keyboard_event(encoded);
        }
    }

    fn machine_keyboard_accepts_input(&self, ctx: &egui::Context) -> bool {
        if self.lldb_session.is_some() && self.lldb_panel.has_input_focus() {
            return false;
        }

        matches!(self.active_view, ActiveView::Display)
            && (self.framebuffer.has_keyboard_focus() || !ctx.wants_keyboard_input())
    }

    fn push_keyboard_event(&mut self, event: u32) {
        if let Some(worker) = self.execution_worker.as_ref() {
            worker.push_keyboard_event(event);
        } else if let Some(session) = self.lldb_session.as_ref() {
            session.push_keyboard_event(event);
        } else {
            self.machine.board_mut().keyboard_mut().push_event(event);
        }
    }
}

fn process_state_label(state: ProcessState) -> &'static str {
    match state {
        ProcessState::Invalid => "invalid",
        ProcessState::Unloaded => "unloaded",
        ProcessState::Connected => "connected",
        ProcessState::Attaching => "attaching",
        ProcessState::Launching => "launching",
        ProcessState::Stopped => "stopped",
        ProcessState::Running => "running",
        ProcessState::Stepping => "stepping",
        ProcessState::Crashed => "crashed",
        ProcessState::Detached => "detached",
        ProcessState::Exited => "exited",
        ProcessState::Suspended => "suspended",
        ProcessState::Unknown(_) => "unknown",
    }
}

pub fn run() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1180.0, 760.0])
            .with_min_inner_size([860.0, 560.0]),
        ..Default::default()
    };
    eframe::run_native(
        "Bedrock Emulator",
        options,
        Box::new(|cc| {
            cc.egui_ctx.set_visuals(egui::Visuals::dark());
            Ok(Box::<BedrockGuiApp>::default())
        }),
    )
}

fn encode_key_event(code: u16, pressed: bool, modifiers: egui::Modifiers) -> u32 {
    let mut event = u32::from(code);
    if pressed {
        event |= 1 << 16;
    }
    if modifiers.shift {
        event |= 1 << 17;
    }
    if modifiers.ctrl {
        event |= 1 << 18;
    }
    if modifiers.alt {
        event |= 1 << 19;
    }
    if modifiers.mac_cmd || modifiers.command {
        event |= 1 << 20;
    }
    event
}

fn encode_input_events(events: &[egui::Event], _text_modifiers: egui::Modifiers) -> Vec<u32> {
    let mut encoded = Vec::new();

    for event in events {
        if let egui::Event::Key {
            key,
            pressed,
            modifiers,
            ..
        } = event
        {
            if let Some(code) = text_key_code(*key, *modifiers) {
                encoded.push(encode_key_event(code, *pressed, *modifiers));
            } else {
                encoded.push(encode_key_event(key_code(*key), *pressed, *modifiers));
            }
        }
    }

    encoded
}

#[cfg(test)]
fn encode_input_event(event: &egui::Event, text_modifiers: egui::Modifiers) -> Vec<u32> {
    encode_input_events(std::slice::from_ref(event), text_modifiers)
}

fn text_key_code(key: egui::Key, modifiers: egui::Modifiers) -> Option<u16> {
    if modifiers.ctrl || modifiers.alt || modifiers.mac_cmd || modifiers.command {
        return None;
    }

    use egui::Key;

    let shifted = modifiers.shift;
    let code = match key {
        Key::Space => b' ',
        Key::Colon => b':',
        Key::Comma => {
            if shifted {
                b'<'
            } else {
                b','
            }
        }
        Key::Backslash => {
            if shifted {
                b'|'
            } else {
                b'\\'
            }
        }
        Key::Slash => {
            if shifted {
                b'?'
            } else {
                b'/'
            }
        }
        Key::Pipe => b'|',
        Key::Questionmark => b'?',
        Key::OpenBracket => {
            if shifted {
                b'{'
            } else {
                b'['
            }
        }
        Key::CloseBracket => {
            if shifted {
                b'}'
            } else {
                b']'
            }
        }
        Key::Backtick => {
            if shifted {
                b'~'
            } else {
                b'`'
            }
        }
        Key::Minus => {
            if shifted {
                b'_'
            } else {
                b'-'
            }
        }
        Key::Period => {
            if shifted {
                b'>'
            } else {
                b'.'
            }
        }
        Key::Plus => b'+',
        Key::Equals => {
            if shifted {
                b'+'
            } else {
                b'='
            }
        }
        Key::Semicolon => {
            if shifted {
                b':'
            } else {
                b';'
            }
        }
        Key::Quote => {
            if shifted {
                b'"'
            } else {
                b'\''
            }
        }
        Key::Num0 => {
            if shifted {
                b')'
            } else {
                b'0'
            }
        }
        Key::Num1 => {
            if shifted {
                b'!'
            } else {
                b'1'
            }
        }
        Key::Num2 => {
            if shifted {
                b'@'
            } else {
                b'2'
            }
        }
        Key::Num3 => {
            if shifted {
                b'#'
            } else {
                b'3'
            }
        }
        Key::Num4 => {
            if shifted {
                b'$'
            } else {
                b'4'
            }
        }
        Key::Num5 => {
            if shifted {
                b'%'
            } else {
                b'5'
            }
        }
        Key::Num6 => {
            if shifted {
                b'^'
            } else {
                b'6'
            }
        }
        Key::Num7 => {
            if shifted {
                b'&'
            } else {
                b'7'
            }
        }
        Key::Num8 => {
            if shifted {
                b'*'
            } else {
                b'8'
            }
        }
        Key::Num9 => {
            if shifted {
                b'('
            } else {
                b'9'
            }
        }
        Key::A => letter_code(b'a', shifted),
        Key::B => letter_code(b'b', shifted),
        Key::C => letter_code(b'c', shifted),
        Key::D => letter_code(b'd', shifted),
        Key::E => letter_code(b'e', shifted),
        Key::F => letter_code(b'f', shifted),
        Key::G => letter_code(b'g', shifted),
        Key::H => letter_code(b'h', shifted),
        Key::I => letter_code(b'i', shifted),
        Key::J => letter_code(b'j', shifted),
        Key::K => letter_code(b'k', shifted),
        Key::L => letter_code(b'l', shifted),
        Key::M => letter_code(b'm', shifted),
        Key::N => letter_code(b'n', shifted),
        Key::O => letter_code(b'o', shifted),
        Key::P => letter_code(b'p', shifted),
        Key::Q => letter_code(b'q', shifted),
        Key::R => letter_code(b'r', shifted),
        Key::S => letter_code(b's', shifted),
        Key::T => letter_code(b't', shifted),
        Key::U => letter_code(b'u', shifted),
        Key::V => letter_code(b'v', shifted),
        Key::W => letter_code(b'w', shifted),
        Key::X => letter_code(b'x', shifted),
        Key::Y => letter_code(b'y', shifted),
        Key::Z => letter_code(b'z', shifted),
        _ => return None,
    };

    Some(u16::from(code))
}

fn letter_code(lowercase: u8, shifted: bool) -> u8 {
    if shifted {
        lowercase.to_ascii_uppercase()
    } else {
        lowercase
    }
}

fn key_code(key: egui::Key) -> u16 {
    use egui::Key;

    match key {
        Key::ArrowDown => 0x0101,
        Key::ArrowLeft => 0x0102,
        Key::ArrowRight => 0x0103,
        Key::ArrowUp => 0x0104,
        Key::Escape => 0x001b,
        Key::Tab => 0x0009,
        Key::Backspace => 0x0008,
        Key::Enter => 0x000d,
        Key::Space => 0x0020,
        Key::Insert => 0x0110,
        Key::Delete => 0x007f,
        Key::Home => 0x0111,
        Key::End => 0x0112,
        Key::PageUp => 0x0113,
        Key::PageDown => 0x0114,
        Key::Copy => 0x0120,
        Key::Cut => 0x0121,
        Key::Paste => 0x0122,
        Key::Colon => b':' as u16,
        Key::Comma => b',' as u16,
        Key::Backslash => b'\\' as u16,
        Key::Slash => b'/' as u16,
        Key::Pipe => b'|' as u16,
        Key::Questionmark => b'?' as u16,
        Key::OpenBracket => b'[' as u16,
        Key::CloseBracket => b']' as u16,
        Key::Backtick => b'`' as u16,
        Key::Minus => b'-' as u16,
        Key::Period => b'.' as u16,
        Key::Plus => b'+' as u16,
        Key::Equals => b'=' as u16,
        Key::Semicolon => b';' as u16,
        Key::Quote => b'\'' as u16,
        Key::Num0 => b'0' as u16,
        Key::Num1 => b'1' as u16,
        Key::Num2 => b'2' as u16,
        Key::Num3 => b'3' as u16,
        Key::Num4 => b'4' as u16,
        Key::Num5 => b'5' as u16,
        Key::Num6 => b'6' as u16,
        Key::Num7 => b'7' as u16,
        Key::Num8 => b'8' as u16,
        Key::Num9 => b'9' as u16,
        Key::A => b'A' as u16,
        Key::B => b'B' as u16,
        Key::C => b'C' as u16,
        Key::D => b'D' as u16,
        Key::E => b'E' as u16,
        Key::F => b'F' as u16,
        Key::G => b'G' as u16,
        Key::H => b'H' as u16,
        Key::I => b'I' as u16,
        Key::J => b'J' as u16,
        Key::K => b'K' as u16,
        Key::L => b'L' as u16,
        Key::M => b'M' as u16,
        Key::N => b'N' as u16,
        Key::O => b'O' as u16,
        Key::P => b'P' as u16,
        Key::Q => b'Q' as u16,
        Key::R => b'R' as u16,
        Key::S => b'S' as u16,
        Key::T => b'T' as u16,
        Key::U => b'U' as u16,
        Key::V => b'V' as u16,
        Key::W => b'W' as u16,
        Key::X => b'X' as u16,
        Key::Y => b'Y' as u16,
        Key::Z => b'Z' as u16,
        Key::F1 => 0x0201,
        Key::F2 => 0x0202,
        Key::F3 => 0x0203,
        Key::F4 => 0x0204,
        Key::F5 => 0x0205,
        Key::F6 => 0x0206,
        Key::F7 => 0x0207,
        Key::F8 => 0x0208,
        Key::F9 => 0x0209,
        Key::F10 => 0x020a,
        Key::F11 => 0x020b,
        Key::F12 => 0x020c,
        Key::F13 => 0x020d,
        Key::F14 => 0x020e,
        Key::F15 => 0x020f,
        Key::F16 => 0x0210,
        Key::F17 => 0x0211,
        Key::F18 => 0x0212,
        Key::F19 => 0x0213,
        Key::F20 => 0x0214,
        Key::F21 => 0x0215,
        Key::F22 => 0x0216,
        Key::F23 => 0x0217,
        Key::F24 => 0x0218,
        Key::F25 => 0x0219,
        Key::F26 => 0x021a,
        Key::F27 => 0x021b,
        Key::F28 => 0x021c,
        Key::F29 => 0x021d,
        Key::F30 => 0x021e,
        Key::F31 => 0x021f,
        Key::F32 => 0x0220,
        Key::F33 => 0x0221,
        Key::F34 => 0x0222,
        Key::F35 => 0x0223,
    }
}

#[cfg(test)]
mod tests {
    use super::{encode_input_event, encode_input_events, encode_key_event, key_code};

    #[test]
    fn encodes_keyboard_event_bits() {
        let event = encode_key_event(
            key_code(egui::Key::A),
            true,
            egui::Modifiers {
                shift: true,
                ctrl: true,
                ..egui::Modifiers::NONE
            },
        );

        assert_eq!(event & 0xffff, b'A' as u32);
        assert_ne!(event & (1 << 16), 0);
        assert_ne!(event & (1 << 17), 0);
        assert_ne!(event & (1 << 18), 0);
        assert_eq!(event & (1 << 19), 0);
    }

    #[test]
    fn ignores_text_input_events() {
        let events = encode_input_event(
            &egui::Event::Text("a~".to_owned()),
            egui::Modifiers {
                shift: true,
                ..egui::Modifiers::NONE
            },
        );

        assert!(events.is_empty());
    }

    #[test]
    fn encodes_plain_text_keys_from_key_events_and_ignores_ime_text() {
        let events = encode_input_events(
            &[
                egui::Event::Key {
                    key: egui::Key::A,
                    physical_key: None,
                    pressed: true,
                    repeat: false,
                    modifiers: egui::Modifiers::NONE,
                },
                egui::Event::Text("ㅁ".to_owned()),
            ],
            egui::Modifiers::NONE,
        );

        assert_eq!(events.len(), 1);
        assert_eq!(events[0] & 0xffff, b'a' as u32);
        assert_ne!(events[0] & (1 << 16), 0);
    }

    #[test]
    fn ignores_ascii_text_when_text_event_precedes_key_event() {
        let events = encode_input_events(
            &[
                egui::Event::Text("a".to_owned()),
                egui::Event::Key {
                    key: egui::Key::A,
                    physical_key: None,
                    pressed: true,
                    repeat: false,
                    modifiers: egui::Modifiers::NONE,
                },
            ],
            egui::Modifiers::NONE,
        );

        assert_eq!(events.len(), 1);
        assert_eq!(events[0], 0x0001_0061);
    }

    #[test]
    fn ignores_ascii_text_when_text_event_follows_key_event() {
        let events = encode_input_events(
            &[
                egui::Event::Key {
                    key: egui::Key::A,
                    physical_key: None,
                    pressed: true,
                    repeat: false,
                    modifiers: egui::Modifiers::NONE,
                },
                egui::Event::Text("a".to_owned()),
            ],
            egui::Modifiers::NONE,
        );

        assert_eq!(events.len(), 1);
        assert_eq!(events[0], 0x0001_0061);
    }

    #[test]
    fn applies_shift_to_plain_text_key_events() {
        let shifted_a = encode_input_event(
            &egui::Event::Key {
                key: egui::Key::A,
                physical_key: None,
                pressed: true,
                repeat: false,
                modifiers: egui::Modifiers {
                    shift: true,
                    ..egui::Modifiers::NONE
                },
            },
            egui::Modifiers::NONE,
        );
        assert_eq!(shifted_a.len(), 1);
        assert_eq!(shifted_a[0] & 0xffff, b'A' as u32);
        assert_ne!(shifted_a[0] & (1 << 17), 0);

        let shifted_one = encode_input_event(
            &egui::Event::Key {
                key: egui::Key::Num1,
                physical_key: None,
                pressed: true,
                repeat: false,
                modifiers: egui::Modifiers {
                    shift: true,
                    ..egui::Modifiers::NONE
                },
            },
            egui::Modifiers::NONE,
        );
        assert_eq!(shifted_one.len(), 1);
        assert_eq!(shifted_one[0] & 0xffff, b'!' as u32);
        assert_ne!(shifted_one[0] & (1 << 17), 0);
    }

    #[test]
    fn preserves_modified_text_keys_as_chords() {
        let ctrl_a = encode_input_event(
            &egui::Event::Key {
                key: egui::Key::A,
                physical_key: None,
                pressed: true,
                repeat: false,
                modifiers: egui::Modifiers {
                    ctrl: true,
                    ..egui::Modifiers::NONE
                },
            },
            egui::Modifiers::NONE,
        );
        assert_eq!(ctrl_a.len(), 1);
        assert_eq!(ctrl_a[0] & 0xffff, b'A' as u32);
        assert_ne!(ctrl_a[0] & (1 << 18), 0);
    }

    #[test]
    fn ignores_non_ascii_text_events() {
        let events = encode_input_event(&egui::Event::Text("ㅁ".to_owned()), egui::Modifiers::NONE);

        assert!(events.is_empty());
    }

    #[test]
    fn ignores_paste_events() {
        let events = encode_input_event(
            &egui::Event::Paste("test".to_owned()),
            egui::Modifiers::NONE,
        );

        assert!(events.is_empty());
    }

    #[test]
    fn forwards_printable_key_presses_repeats_and_releases_without_filtering_repeat() {
        let events = encode_input_events(
            &[
                egui::Event::Key {
                    key: egui::Key::T,
                    physical_key: None,
                    pressed: true,
                    repeat: false,
                    modifiers: egui::Modifiers::NONE,
                },
                egui::Event::Key {
                    key: egui::Key::T,
                    physical_key: None,
                    pressed: true,
                    repeat: true,
                    modifiers: egui::Modifiers::NONE,
                },
                egui::Event::Key {
                    key: egui::Key::T,
                    physical_key: None,
                    pressed: false,
                    repeat: false,
                    modifiers: egui::Modifiers::NONE,
                },
            ],
            egui::Modifiers::NONE,
        );

        assert_eq!(events, vec![0x0001_0074, 0x0001_0074, 0x0000_0074]);
    }

    #[test]
    fn encodes_non_text_keys_from_key_events() {
        let events = encode_input_event(
            &egui::Event::Key {
                key: egui::Key::Enter,
                physical_key: None,
                pressed: true,
                repeat: false,
                modifiers: egui::Modifiers::NONE,
            },
            egui::Modifiers::NONE,
        );

        assert_eq!(events, vec![0x0001_000d]);
    }
}
