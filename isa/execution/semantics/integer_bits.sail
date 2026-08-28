enum Shift_kind = { ShiftLeft, ShiftRightLogical, ShiftRightArithmetic, RotateLeft, RotateRight }

enum Register_result_extension = { RegisterZeroExtend, RegisterSignExtend }

val register_result_extension : Semantic_operation -> Register_result_extension

scattered function register_result_extension

function width_mask(width : int) -> bits(64) =
    if width == 1 then {
        0x00000000000000FF
    } else {
        if width == 2 then {
            0x000000000000FFFF
        } else {
            if width == 4 then { 0x00000000FFFFFFFF } else { 0xFFFFFFFFFFFFFFFF }
        }
    }

function sign_extend_width(value : bits(64), width : int) -> bits(64) =
    if width == 1 then {
        sail_sign_extend(value[7 .. 0], 64)
    } else {
        if width == 2 then {
            sail_sign_extend(value[15 .. 0], 64)
        } else {
            if width == 4 then {
                sail_sign_extend(value[31 .. 0], 64)
            } else {
                value
            }
        }
    }

function canonical_register_result(operation : Semantic_operation, value : bits(64), width : int) -> bits(64) =
    if register_result_extension(operation) == RegisterSignExtend then {
        sign_extend_width(value, width)
    } else {
        value & width_mask(width)
    }

function width_sign(value : bits(64), width : int) -> bool =
    if width == 1 then {
        value[7] == bitone
    } else {
        if width == 2 then {
            value[15] == bitone
        } else {
            if width == 4 then {
                value[31] == bitone
            } else {
                value[63] == bitone
            }
        }
    }

function flags_value(zero : bool, negative : bool, carry : bool, overflow : bool) -> bits(4) =
      (if zero then bitone else bitzero)
    @ (if negative then bitone else bitzero)
    @ (if carry then bitone else bitzero)
    @ (if overflow then bitone else bitzero)

function shift_result(operation : Shift_kind, value : bits(64), raw_count : bits(64), width : int) -> bits(64) = {
    let width_bits = width * 8;
    let count = tmod_int(unsigned(raw_count[5 .. 0]), width_bits);
    let masked = value & width_mask(width);
    if count == 0 then {
        masked
    } else {
        if operation == ShiftLeft then {
            sail_shiftleft(masked, count) & width_mask(width)
        } else {
            if operation == ShiftRightLogical then {
                sail_shiftright(masked, count)
            } else {
                if operation == ShiftRightArithmetic then {
                    let signed_value : bits(64) = if width == 1 then {
                            sail_sign_extend(masked[7 .. 0], 64)
                        } else {
                            if width == 2 then {
                                sail_sign_extend(masked[15 .. 0], 64)
                            } else {
                                if width == 4 then {
                                    sail_sign_extend(masked[31 .. 0], 64)
                                } else {
                                    masked
                                }
                            }
                        };
                    sail_arith_shiftright(signed_value, count) & width_mask(width)
                } else {
                    if operation == RotateLeft then {
                        (sail_shiftleft(masked, count) | sail_shiftright(masked, width_bits - count)) &
                            width_mask(width)
                    } else {
                        (sail_shiftright(masked, count) | sail_shiftleft(masked, width_bits - count)) &
                            width_mask(width)
                    }
                }
            }
        }
    }
}

val route_environment : (Decoded_instruction, Cpu_state, Transaction_family, Primitive_request_kind, Effect_kind, Commit_kind, bool) -> Execution_result
