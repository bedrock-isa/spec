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
