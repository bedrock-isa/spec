function link_active(state : Cpu_state) -> bool = state.lpa[63] == bitone

function link_pa(state : Cpu_state) -> bits(64) =
  state.lpa & 0x7FFFFFFFFFFFFFFF

union clause Uop_kind = UopLinkInactiveGuard : unit
union clause Uop_kind = UopLinkRead : unit
union clause Uop_kind = UopLinkInstall : unit
union clause Uop_kind = UopLinkClear : unit

function clause execute_uop(UopLinkInactiveGuard(), _, values, instruction,
                            before, speculative) =
  if link_active(speculative) then uop_step_fault(faulted(
    before, instruction.form.operation, InvalidControlTransitionFault,
    "taken call or long return while a resident continuation is active"
  )) else uop_step_continue(speculative, values)

function clause execute_uop(UopLinkRead(), uop, values, instruction,
                            before, speculative) =
  if not_bool(link_active(speculative)) then uop_step_fault(faulted(
    before, instruction.form.operation, InvalidControlTransitionFault,
    "resident continuation is not active"
  )) else match uop_location_write(
    uop.destination, speculative.lpc, 64, instruction.form.operation,
    speculative, values
  ) {
    Some((updated, next_values)) => uop_step_continue(updated, next_values),
    None() => uop_step_fault(faulted(
      before, instruction.form.operation, InvalidControlState,
      "resident continuation destination is unavailable"
    )),
  }

function clause execute_uop(UopLinkInstall(), uop, values, instruction,
                            before, speculative) =
  match (uop_location_read(uop.source0, speculative, values),
         uop_location_read(uop.source1, speculative, values)) {
    (Some(continuation), Some(pa)) => {
      var updated = speculative;
      updated.lpc = continuation;
      updated.lpa = 0x8000000000000000 | (pa & 0x7FFFFFFFFFFFFFFF);
      uop_step_continue(updated, values)
    },
    _ => uop_step_fault(faulted(
      before, instruction.form.operation, InvalidControlState,
      "resident continuation input is unavailable"
    )),
  }

function clause execute_uop(UopLinkClear(), _, values, _, _, speculative) = {
  var updated = speculative;
  updated.lpc = 0x0000000000000000;
  updated.lpa = 0x0000000000000000;
  uop_step_continue(updated, values)
}

function resident_RET_uops(state : Cpu_state) -> list(Uop) = {
  let footprint = if link_pa(state) == 0x0000000000000000 then 8 else 16;
  [|
    uop_make(UopLinkRead(), uop_location_make_none(), uop_location_make_none(),
      uop_location_make_temporary(0), Operand_target, 8, CommitControl),
    uop_make(UopControlProbe(), uop_location_make_temporary(0),
      uop_location_make_segment(0), uop_location_make_none(), Operand_target,
      8, CommitControl),
    uop_make(UopStackAdjust(false), uop_location_make_sp(),
      uop_location_make_none(), uop_location_make_sp(), Operand_target,
      footprint, CommitControl),
    uop_make(UopLinkClear(), uop_location_make_none(), uop_location_make_none(),
      uop_location_make_none(), Operand_target, 8, CommitControl),
    uop_make(UopControlCommit(ControlReturn), uop_location_make_temporary(0),
      uop_location_make_segment(0), uop_location_make_none(), Operand_target,
      8, CommitControl)
  |]
}
