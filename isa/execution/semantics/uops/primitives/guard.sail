union clause Uop_kind = UopPredicateGuard : unit
union clause Uop_kind = UopCountGuard : bool
union clause Uop_kind = UopNextPc : unit

function clause execute_uop(UopPredicateGuard(), _, values, instruction, _, speculative) =
    if predicate_holds(instruction, speculative) then uop_step_continue(speculative, values)
    else uop_step_complete(speculative, CommitControl)

function clause execute_uop(UopNextPc(), uop, values, instruction, before, speculative) =
    match uop_location_write(uop.destination, next_pc(speculative, instruction), 64,
                             instruction.form.operation, speculative, values) {
        Some((updated, next_values)) => uop_step_continue(updated, next_values),
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "next-PC destination is unavailable")),
    }

function clause execute_uop(UopCountGuard(decrement), _, values, instruction, before, speculative) = {
    let condition : int = match condition_field(instruction.fields) { Some(value) => value, None() => 0 };
    if decrement then match operand_named(instruction, Operand_counter) {
        None() => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                                    "missing DJcc counter")),
        Some(counter) => {
            let index = unsigned(counter.value[3 .. 0]);
            let count = sub_bits(speculative.registers[index], 0x0000000000000001);
            var updated = speculative; updated.registers[index] = count;
            if count != 0x0000000000000000 & condition_holds(condition, speculative.flags)
            then uop_step_continue(updated, values) else uop_step_complete(updated, CommitControl)
        },
    }
    else match (operand_named(instruction, Operand_index), operand_named(instruction, Operand_bound)) {
        (Some(index_operand), Some(bound_operand)) => {
            let index = unsigned(index_operand.value[3 .. 0]);
            let bound = unsigned(bound_operand.value[3 .. 0]);
            let next = add_bits(speculative.registers[index], 0x0000000000000001);
            var updated = speculative; updated.registers[index] = next;
            if next != speculative.registers[bound] & condition_holds(condition, speculative.flags)
            then uop_step_continue(updated, values) else uop_step_complete(updated, CommitControl)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "missing IJcc counter operands")),
    }
}
