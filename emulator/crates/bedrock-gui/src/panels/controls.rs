use crate::run_worker::FrameStepBudget;
use bedrock_debug::StepResult;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlPanelState {
    pub elf_path: String,
    pub load_base: String,
    pub reset_pc: String,
    pub breakpoint_addr: String,
    pub steps_per_frame: u64,
    pub steps_per_frame_unlimited: bool,
}

impl Default for ControlPanelState {
    fn default() -> Self {
        Self {
            elf_path: String::new(),
            load_base: "0x0".to_owned(),
            reset_pc: "0x0".to_owned(),
            breakpoint_addr: "0x0".to_owned(),
            steps_per_frame: 1,
            steps_per_frame_unlimited: false,
        }
    }
}

impl ControlPanelState {
    pub(crate) fn step_budget(&self) -> FrameStepBudget {
        if self.steps_per_frame_unlimited {
            FrameStepBudget::Unlimited
        } else {
            FrameStepBudget::limited(self.steps_per_frame)
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct ControlActions {
    pub load_elf: bool,
    pub processor_reset: bool,
    pub system_reset: bool,
    pub step: bool,
    pub toggle_running: bool,
    pub add_breakpoint: bool,
    pub remove_breakpoint: bool,
}

#[allow(clippy::too_many_arguments)]
pub fn show(
    ui: &mut egui::Ui,
    state: &mut ControlPanelState,
    running: bool,
    total_steps: u64,
    last_result: Option<&StepResult>,
    breakpoint_count: usize,
    lldb_active: bool,
    perf_summary: &str,
) -> ControlActions {
    let mut actions = ControlActions::default();
    let load_enabled = !lldb_active && !running;
    let debug_controls_enabled = !running || lldb_active;

    ui.vertical(|ui| {
        ui.horizontal_wrapped(|ui| {
            ui.label("ELF");
            ui.add_sized(
                [360.0, 22.0],
                egui::TextEdit::singleline(&mut state.elf_path),
            );
            ui.label("base");
            ui.add_sized(
                [96.0, 22.0],
                egui::TextEdit::singleline(&mut state.load_base),
            );
            actions.load_elf = ui
                .add_enabled(load_enabled, egui::Button::new("Load"))
                .clicked();

            ui.separator();

            ui.label("PC");
            ui.add_sized(
                [110.0, 22.0],
                egui::TextEdit::singleline(&mut state.reset_pc),
            );
            actions.processor_reset = ui
                .add_enabled(debug_controls_enabled, egui::Button::new("Processor Reset"))
                .clicked();
            actions.system_reset = ui
                .add_enabled(debug_controls_enabled, egui::Button::new("System Reset"))
                .clicked();
            actions.step = ui
                .add_enabled(debug_controls_enabled, egui::Button::new("Step"))
                .clicked();
            actions.toggle_running = ui
                .add_enabled(
                    true,
                    egui::Button::new(if running { "Pause" } else { "Run" }),
                )
                .clicked();
            ui.label("steps/frame");
            ui.add_enabled(
                !state.steps_per_frame_unlimited,
                egui::DragValue::new(&mut state.steps_per_frame)
                    .range(1..=u64::MAX)
                    .speed(1.0),
            );
            ui.checkbox(&mut state.steps_per_frame_unlimited, "unlimited");
        });

        ui.horizontal_wrapped(|ui| {
            ui.label("Breakpoint");
            ui.add_sized(
                [130.0, 22.0],
                egui::TextEdit::singleline(&mut state.breakpoint_addr),
            );
            actions.add_breakpoint = ui
                .add_enabled(debug_controls_enabled, egui::Button::new("Add"))
                .clicked();
            actions.remove_breakpoint = ui
                .add_enabled(debug_controls_enabled, egui::Button::new("Remove"))
                .clicked();

            ui.separator();
            ui.monospace(format!("steps {total_steps}"));
            ui.monospace(format!("breakpoints {breakpoint_count}"));
            if lldb_active {
                ui.monospace("lldb active");
            }
            if let Some(result) = last_result {
                ui.monospace(format!("{result:?}"));
            }
            ui.monospace(perf_summary);
        });
    });

    actions
}
