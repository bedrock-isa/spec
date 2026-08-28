function uop_stack_request_make(
    kind : Primitive_request_kind,
    state : Cpu_state,
    address : bits(64),
    range_end : bits(64),
    access : Transaction_access,
    value : bits(64),
    commit_point : bool,
) -> (
    Primitive_request
) = {
    let point = segment_point(state.segments[2], address);
    struct {
        kind = kind,
        ordinal = 0,
        role = RequestRoleStack,
        domain = RequestDomainStack,
        segment = 2,
        segment_image = state.segments[2],
        width = 8,
        range_start = address,
        range_end = range_end,
        range_length = unsigned(sub_bits(range_end, address)),
        range_wrap = unsigned(range_end) < unsigned(address) & range_end != 0x0000000000000000,
        range_end_at_modulus = range_end == 0x0000000000000000 & address != 0x0000000000000000,
        effective_address = address,
        linear_address = point.linear,
        access = access,
        value = value,
        address_translation = true,
        commit_point = commit_point,
        memory_order = 0,
        cache_policy = 0,
        suppress_fault = false,
        staged_updates = [||],
        selector = 0x0000000000000000,
        expected = 0x0000000000000000,
        desired = 0x0000000000000000,
        auxiliary = 0x0000000000000000,
        body_length = 0,
        payload_bytes = [||],
    }
}

union clause Uop_kind = UopStackRange : bool

function clause execute_uop(UopStackRange(push), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(start) => {
            let end_address = add_bits(start, get_slice_int(64, uop.width, 0));
            uop_step_wait(
                0 - 1,
                uop_stack_request_make(
                    StackRange,
                    speculative,
                    start,
                    end_address,
                    if push then AccessStackWrite else AccessStackRead,
                    0x0000000000000000,
                    false,
                ),
                0x0000000000000000,
            )
        },
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop stack range address is unavailable"),
        ),
    }

union clause Uop_kind = UopStackLoad : int

function clause execute_uop(UopStackLoad(offset), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(base) => {
            let address = add_bits(base, get_slice_int(64, offset, 0));
            uop_step_wait(
                uop.destination.index,
                uop_stack_request_make(
                    MemoryRead,
                    speculative,
                    address,
                    add_bits(address, 0x0000000000000008),
                    AccessStackRead,
                    0x0000000000000000,
                    false,
                ),
                0x0000000000000000,
            )
        },
        None() => uop_step_fault(
            faulted(before, instruction.form.operation, InvalidControlState, "uop stack load address is unavailable"),
        ),
    }

union clause Uop_kind = UopStackStorePair : unit
union clause Uop_kind = UopStackStore : unit

function clause execute_uop(UopStackStore(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values)) {
        (Some(value), Some(address)) => uop_step_wait(0 - 1,
            uop_stack_request_make(MemoryStore, speculative, address,
                add_bits(address, 0x0000000000000008), AccessStackWrite, value, true), value),
        _ => uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "uop stack store input is unavailable")),
    }

function clause execute_uop(UopStackStorePair(), uop, values, instruction, before, speculative) =
    match (
        uop_location_read(uop.source0, speculative, values),
        uop_location_read(uop.source1, speculative, values),
        uop_location_read(uop.destination, speculative, values),
    ) {
        (Some(first), Some(second), Some(address)) => {
            let point = segment_point(speculative.segments[2], address);
            let request = {
                uop_stack_request_make(
                    CompoundMemoryStore,
                    speculative,
                    address,
                    add_bits(address, 0x0000000000000010),
                    AccessStackWrite,
                    second,
                    true,
                ) with
                linear_address = point.linear,
                width = 16,
                range_length = 16,
                desired = first,
                auxiliary = add_bits(address, 0x0000000000000008),
            };
            uop_step_wait(0 - 1, request, second)
        },
        _ => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                InvalidControlState,
                "uop stack pair store input is unavailable",
            ),
        ),
    }

union clause Uop_kind = UopPredicateGuard : unit
union clause Uop_kind = UopCountGuard : bool
union clause Uop_kind = UopNextPc : unit
union clause Uop_kind = UopControlTarget : bool
union clause Uop_kind = UopControlProbe : unit
union clause Uop_kind = UopControlCommit : Control_transfer_uop_operation
union clause Uop_kind = UopFusedJump : Fused_jump_uop_operation
union clause Uop_kind = UopRepeat : unit
union clause Uop_kind = UopEventControl : Event_control_uop_operation

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

function clause execute_uop(UopControlTarget(relative), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        Some(raw) => {
            let target = if relative then add_bits(next_pc(speculative, instruction), raw)
                         else narrow_bits(raw, uop.width);
            match uop_location_write(uop.destination, target, 64, instruction.form.operation,
                                     speculative, values) {
                Some((updated, next_values)) => uop_step_continue(updated, next_values),
                None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                            "control target destination is unavailable")),
            }
        },
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "control target is unavailable")),
    }

function clause execute_uop(UopControlProbe(), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values)) {
        (Some(target), Some(cs_image)) =>
            if not_bool(segment_image_valid(cs_image)) then
                uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                  "invalid target code segment"))
            else uop_step_wait(0 - 1, target_probe_request(0, cs_image, target), target),
        _ => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                               "control probe input is unavailable")),
    }

function clause execute_uop(UopControlCommit(operation), uop, values, instruction, before, speculative) =
    match uop_location_read(uop.source0, speculative, values) {
        None() => uop_step_fault(faulted(before, instruction.form.operation, InvalidControlState,
                                    "control commit target is unavailable")),
        Some(target) => {
            var updated = speculative; updated.pc = target;
            if operation == ControlFarJump | operation == ControlFarCall | operation == ControlFarReturn then
                match uop_location_read(uop.source1, speculative, values) {
                    Some(cs_image) => if segment_image_valid(cs_image) then updated.segments[0] = cs_image
                                      else return uop_step_fault(faulted(before, instruction.form.operation,
                                                       InvalidControlState, "invalid target code segment")),
                    None() => return uop_step_fault(faulted(before, instruction.form.operation,
                                                       InvalidControlState, "missing target code segment")),
                }
            else ();
            uop_step_complete_control(updated, CommitControl)
        },
    }

function clause execute_uop(UopFusedJump(operation), uop, values, instruction, before, speculative) =
    match (uop_location_read(uop.source0, speculative, values),
           uop_location_read(uop.source1, speculative, values),
           uop_location_read(uop.source2, speculative, values), condition_field(instruction.fields)) {
        (Some(source), Some(destination), Some(relative), Some(condition)) => {
            let width = uop.width;
            let temporary_flags = if operation == FusedCompareJump then {
                let (_, flags) = sub_with_flags(destination, source, 0, width); flags
            } else {
                let value = narrow_bits(integer_and_value(destination, source), width);
                flags_value(value == 0x0000000000000000, width_sign(value, width), false, false)
            };
            var updated = speculative;
            updated.pc = if condition_holds(condition, temporary_flags)
                         then add_bits(next_pc(speculative, instruction), relative)
                         else next_pc(speculative, instruction);
            uop_step_complete_control(updated, CommitControl)
        },
        _ => uop_step_fault(faulted(before, instruction.form.operation, IllegalInstruction,
                               "fused conditional jump operands are unavailable")),
    }

function clause execute_uop(UopRepeat(), _, _, instruction, _, speculative) =
    uop_step_delegate(start_repeat_transaction(instruction, speculative))

function clause execute_uop(UopEventControl(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(start_event_control(operation, instruction, speculative))
