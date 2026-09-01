function cfi_landing_enabled(state : Cpu_state) -> bool =
  control_register_value(state, ControlRegister_CFI_CFICTL)[0] == bitone

function cfi_shadow_enabled(state : Cpu_state) -> bool =
  control_register_value(state, ControlRegister_CFI_CFICTL)[1] == bitone

function cfi_segment_range_valid(image : bits(64), start : bits(64), width : int)
  -> bool = {
  let last = add_bits(start, bits_from_int(width - 1));
  width > 0
  & unsigned(last) >= unsigned(start)
  & segment_point(image, start).in_bounds
  & segment_point(image, last).in_bounds
}

function cfi_shadow_segment_valid(image : bits(64)) -> bool =
  segment_image_valid(image) & image[6 .. 1] != 0b000000

function cfi_shadow_push_state_valid(state : Cpu_state) -> bool = {
  let shadow_sp = control_register_value(state, ControlRegister_CFI_CFISP);
  let shadow_segment = control_register_value(state, ControlRegister_CFI_CFISS);
  let next = sub_bits(shadow_sp, 0x0000000000000010);
  cfi_shadow_segment_valid(shadow_segment)
  & (shadow_sp & 0x000000000000000F) == 0x0000000000000000
  & cfi_segment_range_valid(shadow_segment, next, 16)
}

function cfi_shadow_pop_state_valid(state : Cpu_state) -> bool = {
  let shadow_sp = control_register_value(state, ControlRegister_CFI_CFISP);
  let shadow_segment = control_register_value(state, ControlRegister_CFI_CFISS);
  cfi_shadow_segment_valid(shadow_segment)
  & (shadow_sp & 0x000000000000000F) == 0x0000000000000000
  & cfi_segment_range_valid(shadow_segment, shadow_sp, 16)
}
