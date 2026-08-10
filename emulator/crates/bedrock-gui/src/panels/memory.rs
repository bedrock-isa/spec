use crate::parse::{parse_u64, parse_usize};
use bedrock_machine::Machine;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MemoryPanelState {
    pub addr: String,
    pub len: String,
}

impl Default for MemoryPanelState {
    fn default() -> Self {
        Self {
            addr: "0x0".to_owned(),
            len: "0x100".to_owned(),
        }
    }
}

pub fn show(ui: &mut egui::Ui, state: &mut MemoryPanelState, machine: &Machine) {
    let ram = machine.board().ram().as_slice();

    ui.horizontal_wrapped(|ui| {
        ui.heading("Memory");
        ui.monospace(format!("RAM {} bytes", ram.len()));
        ui.label("addr");
        ui.add_sized([120.0, 22.0], egui::TextEdit::singleline(&mut state.addr));
        ui.label("len");
        ui.add_sized([86.0, 22.0], egui::TextEdit::singleline(&mut state.len));
    });
    ui.separator();

    let addr = match parse_u64(&state.addr) {
        Ok(addr) => addr,
        Err(error) => {
            ui.label(format!("Invalid address: {error}"));
            return;
        }
    };
    let len = match parse_usize(&state.len) {
        Ok(len) => len,
        Err(error) => {
            ui.label(format!("Invalid length: {error}"));
            return;
        }
    };
    let Ok(start) = usize::try_from(addr) else {
        ui.label("Address is outside RAM");
        return;
    };
    if start >= ram.len() {
        ui.label("Address is outside RAM");
        return;
    }

    let end = start.saturating_add(len).min(ram.len());
    egui::ScrollArea::both()
        .id_salt("memory_dump_scroll")
        .auto_shrink([false, false])
        .show(ui, |ui| {
            for (row, chunk) in ram[start..end].chunks(16).enumerate() {
                let row_addr = start + row * 16;
                ui.add(
                    egui::Label::new(
                        egui::RichText::new(format_dump_row(row_addr as u64, chunk)).monospace(),
                    )
                    .extend(),
                );
            }
        });
}

fn format_dump_row(addr: u64, bytes: &[u8]) -> String {
    let mut hex = String::new();
    let mut ascii = String::new();

    for index in 0..16 {
        if let Some(byte) = bytes.get(index) {
            hex.push_str(&format!("{byte:02x} "));
            ascii.push(if byte.is_ascii_graphic() || *byte == b' ' {
                *byte as char
            } else {
                '.'
            });
        } else {
            hex.push_str("   ");
            ascii.push(' ');
        }
    }

    format!("0x{addr:08x}: {hex} {ascii}")
}

#[cfg(test)]
mod tests {
    use super::format_dump_row;

    #[test]
    fn formats_hex_dump_rows() {
        let row = format_dump_row(0x1000, b"ABC");

        assert!(row.starts_with("0x00001000: 41 42 43"));
        assert!(row.ends_with("ABC             "));
    }
}
