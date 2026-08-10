use crate::app::LoadedElf;
use bedrock_machine::Machine;
use bedrock_toolchain::LlvmToolchain;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct DisassemblyPanelState {
    source: Option<PathBuf>,
    lines: Vec<String>,
    error: Option<String>,
}

impl DisassemblyPanelState {
    pub fn load_from_llvm(&mut self, path: &Path) -> Result<(), String> {
        self.source = Some(path.to_path_buf());
        self.lines.clear();
        self.error = None;

        let text = match LlvmToolchain::discover().and_then(|toolchain| toolchain.disassemble(path))
        {
            Ok(text) => text,
            Err(error) => {
                let error = error.to_string();
                self.error = Some(error.clone());
                return Err(error);
            }
        };

        self.lines = text.lines().map(str::to_owned).collect();
        Ok(())
    }
}

pub(crate) fn show(
    ui: &mut egui::Ui,
    state: &mut DisassemblyPanelState,
    machine: &Machine,
    loaded_elf: Option<&LoadedElf>,
) {
    ui.horizontal_wrapped(|ui| {
        ui.heading("Disassembly");
        ui.monospace(format!("PC 0x{:016x}", machine.state().pc));
        if let Some(loaded) = loaded_elf {
            ui.label(loaded.path.display().to_string());
        }
    });
    ui.separator();

    if let Some(error) = &state.error {
        ui.label(error);
        return;
    }

    if state.lines.is_empty() {
        ui.label("No objdump output");
        return;
    }

    let pc = machine.state().pc;
    let row_height = ui.text_style_height(&egui::TextStyle::Monospace);
    egui::ScrollArea::both()
        .id_salt("disassembly_listing_scroll")
        .auto_shrink([false, false])
        .show_rows(ui, row_height, state.lines.len(), |ui, row_range| {
            for line in &state.lines[row_range] {
                if line_address(line) == Some(pc) {
                    ui.label(
                        egui::RichText::new(line)
                            .monospace()
                            .background_color(ui.visuals().selection.bg_fill)
                            .color(ui.visuals().selection.stroke.color),
                    );
                } else {
                    ui.monospace(line);
                }
            }
        });
}

fn line_address(line: &str) -> Option<u64> {
    let trimmed = line.trim_start();
    let (raw_addr, _) = trimmed.split_once(':')?;
    let raw_addr = raw_addr.trim();
    if raw_addr.is_empty() || !raw_addr.bytes().all(|byte| byte.is_ascii_hexdigit()) {
        return None;
    }
    u64::from_str_radix(raw_addr, 16).ok()
}

#[cfg(test)]
mod tests {
    use super::line_address;

    #[test]
    fn extracts_objdump_line_addresses() {
        assert_eq!(line_address("    1000:\tnop"), Some(0x1000));
        assert_eq!(line_address("foo:"), None);
        assert_eq!(line_address("Disassembly of section .text:"), None);
    }
}
