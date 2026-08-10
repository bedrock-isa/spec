use bedrock_machine::Machine;

pub struct FramebufferPanelState {
    texture: Option<egui::TextureHandle>,
    dirty_seq: Option<u64>,
    keyboard_focused: bool,
    pub scale: f32,
}

impl Default for FramebufferPanelState {
    fn default() -> Self {
        Self {
            texture: None,
            dirty_seq: None,
            keyboard_focused: false,
            scale: 2.0,
        }
    }
}

impl FramebufferPanelState {
    pub fn invalidate(&mut self) {
        self.dirty_seq = None;
    }

    pub fn has_keyboard_focus(&self) -> bool {
        self.keyboard_focused
    }
}

pub fn show(
    ui: &mut egui::Ui,
    ctx: &egui::Context,
    state: &mut FramebufferPanelState,
    machine: &Machine,
) {
    let framebuffer = machine.board().framebuffer();
    let size = [framebuffer.width() as usize, framebuffer.height() as usize];

    if state.texture.is_none() || state.dirty_seq != Some(framebuffer.dirty_seq()) {
        let rgba = framebuffer.rgb332_rgba();
        let image = egui::ColorImage::from_rgba_unmultiplied(size, &rgba);
        if let Some(texture) = &mut state.texture {
            texture.set(image, egui::TextureOptions::NEAREST);
        } else {
            state.texture =
                Some(ctx.load_texture("bedrock-framebuffer", image, egui::TextureOptions::NEAREST));
        }
        state.dirty_seq = Some(framebuffer.dirty_seq());
    }

    ui.horizontal_wrapped(|ui| {
        ui.heading("Display");
        ui.monospace(format!(
            "{}x{} RGB332",
            framebuffer.width(),
            framebuffer.height()
        ));
        ui.monospace(format!("dirty {}", framebuffer.dirty_seq()));
        ui.label(if framebuffer.is_enabled() {
            "enabled"
        } else {
            "disabled"
        });
        ui.label("scale");
        ui.add(egui::Slider::new(&mut state.scale, 1.0..=6.0).show_value(true));
    });
    ui.separator();

    if let Some(texture) = &state.texture {
        let native = texture.size_vec2();
        let desired = egui::vec2(native.x * state.scale, native.y * state.scale);
        let response = egui::ScrollArea::both()
            .id_salt("framebuffer_display_scroll")
            .auto_shrink([false, false])
            .show(ui, |ui| {
                ui.add(
                    egui::Image::new((texture.id(), native))
                        .fit_to_exact_size(desired)
                        .sense(egui::Sense::click()),
                )
            })
            .inner;

        if response.clicked() {
            response.request_focus();
        }
        state.keyboard_focused = response.has_focus();

        if state.keyboard_focused {
            ui.painter().rect_stroke(
                response.rect.expand(2.0),
                0.0,
                egui::Stroke::new(1.0, ui.visuals().selection.stroke.color),
            );
        }
    } else {
        state.keyboard_focused = false;
    }
}
