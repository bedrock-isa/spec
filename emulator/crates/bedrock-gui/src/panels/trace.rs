use bedrock_debug::Debugger;

pub fn show(ui: &mut egui::Ui, debugger: &Debugger) {
    ui.horizontal_wrapped(|ui| {
        ui.heading("Trace");
        ui.monospace(format!("events {}", debugger.trace().len()));
    });
    ui.separator();

    egui::ScrollArea::both()
        .id_salt("debug_trace_scroll")
        .auto_shrink([false, false])
        .stick_to_bottom(true)
        .show(ui, |ui| {
            for event in debugger.trace() {
                ui.monospace(format!("0x{:016x}  {:?}", event.pc, event.result));
            }
        });
}
