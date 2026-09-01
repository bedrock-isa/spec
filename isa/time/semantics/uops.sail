union clause Uop_kind = UopTime : Time_uop_operation

function clause execute_uop(UopTime(operation), _, _, instruction, before, speculative) =
  if operation == TimeRead then match destination_named(instruction, Operand_dst, 8) {
    Some(destination) => uop_step_complete(write_local_destination(
      speculative, instruction.form.operation, destination, speculative.time.value
    ), CommitRegisters),
    None() => uop_step_fault(faulted(
      before, instruction.form.operation, IllegalInstruction,
      "RDTIME destination is unavailable"
    )),
  }
  else if operation == TimeArm then match (
    value_named(instruction, speculative, Operand_deadline),
    value_named(instruction, speculative, Operand_identity)
  ) {
    (Some(deadline), Some(identity)) =>
      if identity == 0x0000000000000000
         | unsigned(identity) > unsigned(speculative.controls.interrupt_file.max_id) then
        uop_step_fault(faulted(
          before, instruction.form.operation, InvalidControlSelectorFault,
          "TARM interrupt identity is not implemented"
        ))
      else uop_step_complete(
        time_with_arm(speculative, deadline, identity[23 .. 0]), CommitControl
      ),
    _ => uop_step_fault(faulted(
      before, instruction.form.operation, IllegalInstruction,
      "TARM operands are unavailable"
    )),
  }
  else uop_step_complete(time_with_cancel(speculative), CommitControl)
