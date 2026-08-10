use bedrock_core::{CPU_REGISTER_INFOS, CpuRegisterSet, CpuState};
use bedrock_debug::Debugger;
use bedrock_machine::Machine;

pub fn show(ui: &mut egui::Ui, machine: &Machine, debugger: &mut Debugger, controls_enabled: bool) {
    let state = machine.state();

    show_register_group(ui, "CPU", state, CpuRegisterSet::General);
    ui.separator();
    show_register_group(ui, "Segments", state, CpuRegisterSet::Segment);
    ui.separator();
    show_register_group(ui, "Control", state, CpuRegisterSet::Control);
    ui.separator();
    show_register_group(ui, "FPU", state, CpuRegisterSet::FloatingPoint);

    ui.separator();
    ui.heading("Breakpoints");
    let breakpoints: Vec<_> = debugger.breakpoints().all().to_vec();
    if breakpoints.is_empty() {
        ui.label("None");
        return;
    }

    let mut remove_addr = None;
    for breakpoint in breakpoints {
        ui.horizontal(|ui| {
            ui.monospace(format!("0x{:016x}", breakpoint.addr));
            ui.label(if breakpoint.enabled {
                "enabled"
            } else {
                "disabled"
            });
            if ui
                .add_enabled(controls_enabled, egui::Button::new("Remove"))
                .clicked()
            {
                remove_addr = Some(breakpoint.addr);
            }
        });
    }

    if let Some(addr) = remove_addr {
        debugger.breakpoints_mut().remove(addr);
    }
}

fn show_register_group(ui: &mut egui::Ui, heading: &str, state: &CpuState, set: CpuRegisterSet) {
    ui.heading(heading);
    egui::Grid::new(format!("cpu-registers-{}", set.label()))
        .num_columns(2)
        .spacing([12.0, 4.0])
        .show(ui, |ui| {
            for info in CPU_REGISTER_INFOS.iter().filter(|info| info.set == set) {
                register_row(
                    ui,
                    info.name,
                    format_register_value(state.read_register(info.register), info.bits),
                );
            }
        });
}

fn register_row(ui: &mut egui::Ui, name: &str, value: impl Into<String>) {
    ui.label(name);
    ui.monospace(value.into());
    ui.end_row();
}

fn format_register_value(value: u64, bits: u16) -> String {
    let digits = usize::from(bits).div_ceil(4).max(1);
    format!("0x{value:0digits$x}")
}

#[cfg(test)]
mod tests {
    use super::format_register_value;

    #[test]
    fn formats_register_values_by_width() {
        assert_eq!(format_register_value(0xab, 8), "0xab");
        assert_eq!(format_register_value(0xab, 16), "0x00ab");
        assert_eq!(
            format_register_value(0x1122_3344_5566_7788, 64),
            "0x1122334455667788"
        );
    }
}
