struct Lowered_uop_operand = {
  program : list(Micro_operation),
  value : Uop_location,
  address : Uop_location,
  next_temporary : int,
  memory : bool,
}

function make_uop(
    kind : Uop_kind,
    source0 : Uop_location,
    source1 : Uop_location,
    destination : Uop_location,
    operand_name : Operand_id,
    width : int,
    commit_kind : Commit_kind,
) -> (
    Micro_operation
) =
    struct {
        kind = kind,
        source0 = source0,
        source1 = source1,
        destination = destination,
        operand_name = operand_name,
        width = width,
        commit_kind = commit_kind,
    }

function direct_uop_location(operand : Decoded_operand) -> Uop_location =
    if operand.operand_type == OperandType_Rn then {
        uop_register(unsigned(operand.value[3 .. 0]))
    } else {
        if operand.operand_type == OperandType_SP then {
            uop_sp()
        } else {
            if operand.operand_type == OperandType_EA then {
                match operand.ea {
                    Some(ea) => uop_immediate(ea_signed_payload(ea)),
                    None() => uop_none(),
                }
            } else {
                uop_immediate(immediate_value(operand))
            }
        }
    }

function ea_update_location(ea : Decoded_ea) -> option(Uop_location) =
    if ea.update_target == Some(EaUpdateTarget_b) & ea.base == Some(EaBase_SP) then {
        Some(uop_sp())
    } else {
        if ea.update_target == Some(EaUpdateTarget_b) then {
            match ea_field_role(EaRole_base, ea.fields) {
                Some(index) => Some(uop_register(index)),
                None() => None(),
            }
        } else {
            if ea.update_target == Some(EaUpdateTarget_i) then {
                match ea_field_role(EaRole_index, ea.fields) {
                    Some(index) => Some(uop_register(index)),
                    None() => None(),
                }
            } else {
                None()
            }
        }
    }

function ea_update_program(operand : Decoded_operand, width : int, pre : bool) -> list(Micro_operation) =
    match operand.ea {
        None() => [||],
        Some(ea) => {
            let selected = if pre then {
                    ea.update_mode == Some(EaUpdateMode_predecrement)
                } else {
                    ea.update_mode == Some(EaUpdateMode_postincrement)
                };
            if not_bool(selected) then {
                [||]
            } else {
                match ea_update_location(ea) {
                    None() => [||],
                    Some(destination) => {
                        let magnitude = if ea.update_target == Some(EaUpdateTarget_i) then { 1 } else { width };
                        let amount = if pre then {
                                bits_from_int(0 - magnitude)
                            } else {
                                bits_from_int(magnitude)
                            };
                        [|
                            make_uop(
                                UopIntegerAdd(),
                                destination,
                                uop_immediate(amount),
                                destination,
                                operand.name,
                                8,
                                CommitRegisters,
                            ),
                        |]
                    },
                }
            }
        },
    }

function lower_uop_operand(
    operand : Decoded_operand,
    width : int,
    next_temporary : int,
    read_memory : bool,
) -> (
    Lowered_uop_operand
) =
    match operand.ea {
        Some(ea) => if ea.kind == EaKind_memory then {
            let address = uop_temporary(next_temporary);
            let value = if read_memory then {
                    uop_temporary(next_temporary + 1)
                } else {
                    uop_none()
                };
            let calculate = [|make_uop(UopCalcEa(), uop_none(), uop_none(), address, operand.name, width, CommitNone)|];
            let load = if read_memory then {
                    [|make_uop(UopMemoryLoad(), address, uop_none(), value, operand.name, width, CommitMemory)|]
                } else {
                    [||]
                };
            struct {
                program =
                    append_uops(
                        ea_update_program(operand, width, true),
                        append_uops(calculate, append_uops(ea_update_program(operand, width, false), load)),
                    ),
                value = value,
                address = address,
                next_temporary = next_temporary + (if read_memory then 2 else 1),
                memory = true,
            }
        } else {
            struct {
                program = [||],
                value = direct_uop_location(operand),
                address = uop_none(),
                next_temporary = next_temporary,
                memory = false,
            }
        },
        None() => struct {
            program = [||],
            value = direct_uop_location(operand),
            address = uop_none(),
            next_temporary = next_temporary,
            memory = false,
        },
    }
