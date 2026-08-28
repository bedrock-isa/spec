function uop_none() -> Uop_location = struct { kind = UopLocationNone, index = 0, immediate = 0x0000000000000000 }

function uop_register(index : int) -> Uop_location = struct {
    kind = UopLocationRegister,
    index = index,
    immediate = 0x0000000000000000,
}

function uop_fp_register(index : int) -> Uop_location = struct {
    kind = UopLocationFpRegister,
    index = index,
    immediate = 0x0000000000000000,
}

function uop_sp() -> Uop_location = struct { kind = UopLocationSp, index = 0, immediate = 0x0000000000000000 }

function uop_immediate(value : bits(64)) -> Uop_location = struct {
    kind = UopLocationImmediate,
    index = 0,
    immediate = value,
}

function uop_temporary(index : int) -> Uop_location = struct {
    kind = UopLocationTemporary,
    index = index,
    immediate = 0x0000000000000000,
}

function empty_uop_value() -> Uop_value = struct {
    value = 0x0000000000000000,
    secondary_value = 0x0000000000000000,
    flags = 0x0,
    write_flags = false,
    generated_fflags = 0b00000,
    bounds_passed = false,
    cache_policy = 0,
    access_class = NormalAccess,
    physical_class = NormalPhysical,
    atomic_store_happened = false,
    body_bytes = [||],
    known = false,
    present = false,
    address = false,
    segment = 0,
    segment_image = 0x0000000000000000,
    effective_address = 0x0000000000000000,
    linear_address = 0x0000000000000000,
    domain = RequestDomainCurrent,
}

function uop_value_at(values : list(Uop_value), index : int) -> option(Uop_value) =
    match values {
        [||] => None(),
        value :: tail => if index <= 0 then {
            Some(value)
        } else {
            uop_value_at(tail, index - 1)
        },
    }

function uop_value_set(values : list(Uop_value), index : int, value : Uop_value) -> list(Uop_value) =
    if index < 0 then {
        values
    } else {
        match values {
            [||] => if index == 0 then {
                [|value|]
            } else {
                empty_uop_value() :: uop_value_set([||], index - 1, value)
            },
            head :: tail => if index == 0 then {
                value :: tail
            } else {
                head :: uop_value_set(tail, index - 1, value)
            },
        }
    }

function append_uops(left : list(Micro_operation), right : list(Micro_operation)) -> list(Micro_operation) =
    match left {
        [||] => right,
        head :: tail => head :: append_uops(tail, right),
    }

function uop_location_value(location : Uop_location, state : Cpu_state, values : list(Uop_value)) -> option(bits(64)) =
    if location.kind == UopLocationRegister then {
        Some(state.registers[unsigned(get_slice_int(4, location.index, 0))])
    } else {
        if location.kind == UopLocationFpRegister then {
            Some(state.floating_registers[unsigned(get_slice_int(4, location.index, 0))])
        } else {
            if location.kind == UopLocationSp then {
                Some(state.sp)
            } else {
                if location.kind == UopLocationImmediate then {
                    Some(location.immediate)
                } else {
                    if location.kind == UopLocationTemporary then {
                        match uop_value_at(values, location.index) {
                            Some(value) => Some(value.value),
                            None() => None(),
                        }
                    } else {
                        None()
                    }
                }
            }
        }
    }

function uop_write_location(
    location : Uop_location,
    value : bits(64),
    width : int,
    operation : Semantic_operation,
    state : Cpu_state,
    values : list(Uop_value),
) -> (
    option((Cpu_state, list(Uop_value)))
) = {
    var updated = state;
    if location.kind == UopLocationRegister then {
        updated.registers[unsigned(get_slice_int(4, location.index, 0))] = canonical_register_result(
            operation,
            value,
            width,
        );
        Some((updated, values))
    } else {
        if location.kind == UopLocationSp then {
            updated.sp = value;
            Some((updated, values))
        } else {
            if location.kind == UopLocationTemporary then {
                Some((updated, uop_value_set(values, location.index, { empty_uop_value() with value = value })))
            } else {
                None()
            }
        }
    }
}

function uop_at(program : list(Micro_operation), cursor : int) -> option(Micro_operation) =
    match program {
        [||] => None(),
        operation :: tail => if cursor <= 0 then {
            Some(operation)
        } else {
            uop_at(tail, cursor - 1)
        },
    }

function uop_memory_request(
    kind : Primitive_request_kind,
    address : Uop_value,
    width : int,
    access : Transaction_access,
    value : bits(64),
    commit_point : bool,
) -> (
    Primitive_request
) =
    struct {
        kind = kind,
        ordinal = 0,
        role = RequestRoleValue,
        domain = address.domain,
        segment = address.segment,
        segment_image = address.segment_image,
        width = width,
        range_start = address.effective_address,
        range_end = add_bits(address.effective_address, get_slice_int(64, width, 0)),
        range_length = width,
        range_wrap = unsigned(address.effective_address) + width > 18446744073709551616,
        range_end_at_modulus = unsigned(address.effective_address) + width == 18446744073709551616,
        effective_address = address.effective_address,
        linear_address = address.linear_address,
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

function waiting_uop(
    program : list(Micro_operation),
    cursor : int,
    values : list(Uop_value),
    pending_destination : int,
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
    phase : Continuation_phase,
    request : Primitive_request,
    captured : bits(64),
) -> (
    Execution_result
) =
    struct {
        state = before,
        pending =
            {
                empty_pending(Some(speculative), instruction.form.operation, CommitMemory) with
                instruction = Some(instruction),
                phase = phase,
                captured_first = captured,
                uop_program = program,
                uop_cursor = cursor,
                uop_values = values,
                uop_pending_destination = pending_destination,
            },
        request = request,
        effects = [||],
        fault = None(),
        awaiting_environment = true,
    }

val run_uop_program : (list(Micro_operation), int, list(Uop_value), Decoded_instruction, Cpu_state, Cpu_state) -> Execution_result

val execute_uop : (Uop_kind, Micro_operation, list(Uop_value), Decoded_instruction, Cpu_state, Cpu_state) -> Uop_step

scattered function execute_uop

function uop_continue(state : Cpu_state, values : list(Uop_value)) -> Uop_step =
    UopContinue(struct { state = state, values = values })

function uop_wait(pending_destination : int, request : Primitive_request, captured : bits(64)) -> Uop_step =
    UopWait(struct { pending_destination = pending_destination, request = request, captured = captured })

function uop_complete(state : Cpu_state, commit_kind : Commit_kind) -> Uop_step =
    UopComplete(struct { state = state, commit_kind = commit_kind })

function uop_fault(result : Execution_result) -> Uop_step = UopFault(result)

function uop_delegate(result : Execution_result) -> Uop_step = UopDelegate(result)

function uop_local_result_step(
    result : Execution_result,
    speculative : Cpu_state,
    values : list(Uop_value),
) -> (
    Uop_step
) =
    match result.fault {
        Some(_) => uop_fault(result),
        None() => if result.awaiting_environment then {
            uop_delegate(result)
        } else {
            var updated = result.state;
            updated.pc = speculative.pc;
            uop_continue(updated, values)
        },
    }

function interpret_uop_step(
    step : Uop_step,
    program : list(Micro_operation),
    cursor : int,
    values : list(Uop_value),
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
) -> (
    Execution_result
) =
    match step {
        UopContinue(next) => run_uop_program(program, cursor + 1, next.values, instruction, before, next.state),
        UopWait(wait) => waiting_uop(
            program,
            cursor + 1,
            values,
            wait.pending_destination,
            instruction,
            before,
            speculative,
            PhaseUopWait,
            wait.request,
            wait.captured,
        ),
        UopComplete(done) => completed(before, advance_pc(done.state, instruction), done.commit_kind, [||]),
        UopDelegate(result) => result,
        UopFault(result) => result,
    }

function run_uop_program(
    program : list(Micro_operation),
    cursor : int,
    values : list(Uop_value),
    instruction : Decoded_instruction,
    before : Cpu_state,
    speculative : Cpu_state,
) -> (
    Execution_result
) =
    match uop_at(program, cursor) {
        None() => faulted(before, instruction.form.operation, InvalidControlState, "uop program ended without commit"),
        Some(uop) => interpret_uop_step(
            execute_uop(uop.kind, uop, values, instruction, before, speculative),
            program,
            cursor,
            values,
            instruction,
            before,
            speculative,
        ),
    }

function execute_uop_program(
    program : list(Micro_operation),
    instruction : Decoded_instruction,
    state : Cpu_state,
) -> (
    Execution_result
) =
    run_uop_program(program, 0, [||], instruction, state, state)

function preserve_uop_parent(next : Execution_result, previous : Execution_result) -> Execution_result =
    if not_bool(next.awaiting_environment) then {
        next
    } else {
        {
            next with
            pending =
                {
                    next.pending with
                    repeat_body = previous.pending.repeat_body,
                    repeat_bytes = previous.pending.repeat_bytes,
                    repeat_parent_active = previous.pending.repeat_parent_active,
                    boundary_class = previous.pending.boundary_class,
                },
        }
    }

function resume_uop_phase(previous : Execution_result, response : Transaction_response) -> Execution_result =
    match previous.pending.instruction {
        None() => faulted(
            previous.state,
            previous.pending.operation,
            InvalidControlState,
            "uop continuation has no instruction",
        ),
        Some(instruction) => {
            let values = if previous.pending.uop_pending_destination >= 0 then {
                    uop_value_set(
                        previous.pending.uop_values,
                        previous.pending.uop_pending_destination,
                        struct {
                            value = response.value,
                            secondary_value = response.secondary_value,
                            flags = response.flags,
                            write_flags = response.write_flags,
                            generated_fflags = response.generated_fflags,
                            bounds_passed = response.bounds_passed,
                            cache_policy = response.cache_policy,
                            access_class = response.access_class,
                            physical_class = response.physical_class,
                            atomic_store_happened = response.atomic_store_happened,
                            body_bytes = response.body_bytes,
                            known = response.known,
                            present = response.present,
                            address = false,
                            segment = 0,
                            segment_image = 0x0000000000000000,
                            effective_address = 0x0000000000000000,
                            linear_address = 0x0000000000000000,
                            domain = RequestDomainCurrent,
                        },
                    )
                } else {
                    previous.pending.uop_values
                };
            preserve_uop_parent(
                run_uop_program(
                    previous.pending.uop_program,
                    previous.pending.uop_cursor,
                    values,
                    instruction,
                    previous.state,
                    pending_after(previous),
                ),
                previous,
            )
        },
    }
