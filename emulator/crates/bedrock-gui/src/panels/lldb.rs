const SCROLLBACK_LIMIT: usize = 512;

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct LldbPanelState {
    input: String,
    history: Vec<String>,
    history_cursor: Option<usize>,
    lines: Vec<ConsoleLine>,
    process_state: String,
    input_has_focus: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct ConsoleLine {
    kind: ConsoleLineKind,
    text: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ConsoleLineKind {
    Prompt,
    Output,
    Error,
    Status,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct LldbPanelActions {
    pub start: bool,
    pub submit: Option<String>,
    pub detach: bool,
}

impl LldbPanelState {
    pub fn push_prompt(&mut self, command: &str) {
        self.push(ConsoleLineKind::Prompt, format!("(lldb) {command}"));
    }

    pub fn push_output(&mut self, output: &str) {
        self.push_multiline(ConsoleLineKind::Output, output);
    }

    pub fn push_error(&mut self, output: &str) {
        self.push_multiline(ConsoleLineKind::Error, output);
    }

    pub fn push_status(&mut self, output: impl Into<String>) {
        self.push(ConsoleLineKind::Status, output.into());
    }

    pub fn set_process_state(&mut self, state: impl Into<String>) {
        self.process_state = state.into();
    }

    pub fn has_input_focus(&self) -> bool {
        self.input_has_focus
    }

    fn push_multiline(&mut self, kind: ConsoleLineKind, output: &str) {
        for line in output.lines() {
            self.push(kind, line.to_owned());
        }
    }

    fn push(&mut self, kind: ConsoleLineKind, text: String) {
        self.lines.push(ConsoleLine { kind, text });
        if self.lines.len() > SCROLLBACK_LIMIT {
            self.lines.remove(0);
        }
    }

    fn submit_current_input(&mut self) -> Option<String> {
        let command = self.input.trim().to_owned();
        if command.is_empty() {
            return None;
        }
        self.history.push(command.clone());
        self.history_cursor = None;
        self.input.clear();
        Some(command)
    }

    fn history_previous(&mut self) {
        if self.history.is_empty() {
            return;
        }
        let index = self
            .history_cursor
            .map(|index| index.saturating_sub(1))
            .unwrap_or_else(|| self.history.len().saturating_sub(1));
        self.history_cursor = Some(index);
        self.input = self.history[index].clone();
    }

    fn history_next(&mut self) {
        let Some(index) = self.history_cursor else {
            return;
        };
        let next = index + 1;
        if next >= self.history.len() {
            self.history_cursor = None;
            self.input.clear();
        } else {
            self.history_cursor = Some(next);
            self.input = self.history[next].clone();
        }
    }
}

pub fn show(ui: &mut egui::Ui, state: &mut LldbPanelState, active: bool) -> LldbPanelActions {
    let mut actions = LldbPanelActions::default();
    let panel_size = ui.available_size();
    ui.set_min_size(panel_size);

    ui.horizontal_wrapped(|ui| {
        ui.heading("LLDB");
        if state.process_state.is_empty() {
            ui.monospace(if active { "starting" } else { "inactive" });
        } else {
            ui.monospace(&state.process_state);
        }
        if active {
            actions.detach = ui.button("Detach").clicked();
        } else {
            actions.start = ui.button("Start").clicked();
        }
    });
    ui.separator();

    let input_row_height = ui.spacing().interact_size.y.max(26.0) + ui.spacing().item_spacing.y;
    let reserved_input_strip = input_row_height + ui.spacing().item_spacing.y * 2.0 + 4.0;
    let scroll_height = (ui.available_height() - reserved_input_strip).max(24.0);
    ui.allocate_ui_with_layout(
        egui::vec2(ui.available_width(), scroll_height),
        egui::Layout::top_down(egui::Align::Min),
        |ui| {
            egui::ScrollArea::both()
                .id_salt("lldb_scrollback")
                .auto_shrink([false, false])
                .stick_to_bottom(true)
                .show(ui, |ui| {
                    for line in &state.lines {
                        match line.kind {
                            ConsoleLineKind::Prompt => {
                                ui.monospace(&line.text);
                            }
                            ConsoleLineKind::Output => {
                                ui.monospace(&line.text);
                            }
                            ConsoleLineKind::Error => {
                                ui.colored_label(ui.visuals().error_fg_color, &line.text);
                            }
                            ConsoleLineKind::Status => {
                                ui.colored_label(ui.visuals().weak_text_color(), &line.text);
                            }
                        }
                    }
                });
        },
    );

    ui.separator();
    ui.allocate_ui_with_layout(
        egui::vec2(ui.available_width(), input_row_height),
        egui::Layout::left_to_right(egui::Align::Center),
        |ui| {
            ui.monospace("(lldb)");
            let response = ui.add_enabled(
                active,
                egui::TextEdit::singleline(&mut state.input)
                    .desired_width(f32::INFINITY)
                    .hint_text("command"),
            );
            state.input_has_focus = response.has_focus();
            if state.input_has_focus {
                if ui.input(|input| input.key_pressed(egui::Key::ArrowUp)) {
                    state.history_previous();
                }
                if ui.input(|input| input.key_pressed(egui::Key::ArrowDown)) {
                    state.history_next();
                }
            }
            if response.lost_focus() && ui.input(|input| input.key_pressed(egui::Key::Enter)) {
                actions.submit = state.submit_current_input();
            }
        },
    );

    actions
}
