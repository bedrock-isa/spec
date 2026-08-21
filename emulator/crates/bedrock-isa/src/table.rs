#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum EncodingClass {
    ExtraShort,
    Short,
    Medium,
    Long,
    ExtraLong,
}

impl EncodingClass {
    pub const fn opcode_bytes(self) -> usize {
        match self {
            Self::ExtraShort => 1,
            Self::Short => 2,
            Self::Medium => 3,
            Self::Long => 4,
            Self::ExtraLong => 5,
        }
    }

    pub const fn payload_bits(self) -> u8 {
        match self {
            Self::ExtraShort => 7,
            Self::Short => 14,
            Self::Medium => 18,
            Self::Long => 26,
            Self::ExtraLong => 34,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FieldKind {
    Rn,
    Freg,
    Ea7,
    Condition,
    Size,
    Immediate,
    Bits,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GeneratedField {
    pub symbol: char,
    pub kind: FieldKind,
    pub width: u8,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GeneratedEaField {
    pub symbol: char,
    pub syntax_operand_ordinal: u8,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GeneratedConstraint {
    Allow {
        field: char,
        ranges: &'static [(u64, u64)],
        reason: &'static str,
    },
    Exclude {
        field: Option<char>,
        destination: bool,
        predicate: ConstraintPredicate,
        reason: &'static str,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConstraintPredicate {
    RnDirect,
    SpDirect,
    RegDirect,
    Immediate,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InstructionSet {
    Base,
    Fpu,
    FpuTranscendental,
    VirtualizationAcceleration,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FlagsEffect {
    Unchanged,
    Writes,
    Body,
    Grouped,
    OperationDefined,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RepeatOperandLocation {
    Rn,
    EffectiveAddress,
    StackPointer,
    SegmentRegister,
    CodeSegment,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RepeatObservedOperand {
    pub name: &'static str,
    pub field: Option<char>,
    pub location: RepeatOperandLocation,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RepeatObservation {
    Computed,
    Result { operand: RepeatObservedOperand },
    Source { operand: RepeatObservedOperand },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DestinationOverlapRule {
    SameValue,
    IllegalInstruction,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GeneratedDestinationOverlap {
    pub operands: [&'static str; 2],
    pub operand_fields: [char; 2],
    pub rule: DestinationOverlapRule,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GeneratedAttributes {
    pub instruction_set: InstructionSet,
    pub privileged: bool,
    pub repeat_rep: bool,
    pub repeat_repcc: bool,
    pub repeat_repg: bool,
    pub repeat_observed: Option<RepeatObservation>,
    pub flags: FlagsEffect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GeneratedForm {
    pub form: crate::generated::FormId,
    pub id: &'static str,
    pub opcode: crate::generated::Opcode,
    pub text: &'static str,
    pub class: EncodingClass,
    pub payload_bits: u8,
    pub fixed_operand_bytes: u8,
    pub pattern: &'static str,
    pub mask: u64,
    pub value: u64,
    pub fields: &'static [GeneratedField],
    pub ea_fields: &'static [GeneratedEaField],
    pub constraints: &'static [GeneratedConstraint],
    pub destination_overlap: &'static [GeneratedDestinationOverlap],
    pub attributes: GeneratedAttributes,
}

pub fn extract_pattern_field(pattern: &str, field: char, payload: u64) -> Option<u64> {
    let mut value = 0u64;
    let mut width = 0u8;
    let pattern_width = pattern.len();
    for (index, symbol) in pattern.chars().enumerate() {
        if symbol != field {
            continue;
        }
        let bit_index = pattern_width - index - 1;
        value = (value << 1) | ((payload >> bit_index) & 1);
        width += 1;
    }
    (width != 0).then_some(value)
}

pub fn form_accepts(form: &GeneratedForm, payload: u64) -> bool {
    if payload & form.mask != form.value {
        return false;
    }
    form.constraints.iter().all(|constraint| match constraint {
        GeneratedConstraint::Allow { field, ranges, .. } => {
            let Some(value) = extract_pattern_field(form.pattern, *field, payload) else {
                return false;
            };
            ranges.iter().any(|(lo, hi)| *lo <= value && value <= *hi)
        }
        GeneratedConstraint::Exclude {
            field,
            destination,
            predicate,
            ..
        } => {
            let field = if *destination {
                form.fields
                    .iter()
                    .find(|candidate| candidate.width == 7 && matches!(candidate.symbol, 'd' | 'e'))
                    .map(|candidate| candidate.symbol)
            } else {
                *field
            };
            let Some(value) =
                field.and_then(|field| extract_pattern_field(form.pattern, field, payload))
            else {
                return false;
            };
            !matches_predicate(*predicate, value)
        }
    })
}

fn matches_predicate(predicate: ConstraintPredicate, value: u64) -> bool {
    match predicate {
        ConstraintPredicate::RnDirect => value <= 0x0f,
        ConstraintPredicate::SpDirect => value == 0x68,
        ConstraintPredicate::RegDirect => value <= 0x0f || value == 0x68,
        ConstraintPredicate::Immediate => (0x5b..=0x5e).contains(&value),
    }
}

#[cfg(test)]
mod tests {
    use super::{
        DestinationOverlapRule, FieldKind, GeneratedConstraint, RepeatObservation,
        RepeatObservedOperand, RepeatOperandLocation, extract_pattern_field, form_accepts,
    };
    use crate::EncodingClass;
    use crate::generated::{
        EXTRALONG_LOOKUP_MAX_DEPTH, FormId, GENERATED_FORMS, LONG_LOOKUP_MAX_DEPTH, decode_form,
    };

    #[test]
    fn extracts_split_field_in_display_order() {
        assert_eq!(
            extract_pattern_field("0eee10z0000000eeee", 'e', 0b01_0110_0000_0000_0110),
            Some(0b1010110)
        );
    }

    #[test]
    fn every_generated_form_has_a_unique_constraint_valid_representative() {
        for form in GENERATED_FORMS {
            let mut payload = form.value;
            for constraint in form.constraints {
                match constraint {
                    GeneratedConstraint::Allow { field, ranges, .. } => {
                        payload = set_field(form.pattern, *field, payload, ranges[0].0);
                    }
                    GeneratedConstraint::Exclude {
                        field, destination, ..
                    } => {
                        let symbol = if *destination {
                            form.fields
                                .iter()
                                .find(|candidate| {
                                    candidate.width == 7 && matches!(candidate.symbol, 'd' | 'e')
                                })
                                .unwrap()
                                .symbol
                        } else {
                            field.unwrap()
                        };
                        payload = set_field(form.pattern, symbol, payload, 0x10);
                    }
                }
            }
            assert!(
                form_accepts(form, payload),
                "{} representative rejected",
                form.id
            );
            let count = GENERATED_FORMS
                .iter()
                .filter(|candidate| {
                    candidate.class == form.class && form_accepts(candidate, payload)
                })
                .count();
            assert_eq!(count, 1, "{} representative is ambiguous", form.id);
            assert_eq!(
                decode_form(form.class, payload).map(|decoded| decoded.form),
                Some(form.form),
                "{} decision lookup disagrees with form matcher",
                form.id
            );
        }
    }

    #[test]
    fn generated_forms_preserve_every_repeat_observation_kind() {
        assert_eq!(
            form("short.cmp_x_rn_s_rn_d").attributes.repeat_observed,
            Some(RepeatObservation::Computed)
        );
        assert_eq!(
            form("short.add_x_rn_s_rn_d").attributes.repeat_observed,
            Some(RepeatObservation::Result {
                operand: RepeatObservedOperand {
                    name: "dst",
                    field: Some('d'),
                    location: RepeatOperandLocation::Rn,
                },
            })
        );
        assert_eq!(
            form("long.movnt_x_rn_s_ea_e").attributes.repeat_observed,
            Some(RepeatObservation::Source {
                operand: RepeatObservedOperand {
                    name: "src",
                    field: Some('s'),
                    location: RepeatOperandLocation::Rn,
                },
            })
        );
        assert_eq!(
            form("medium.add_x_rn_s_ea_e").attributes.repeat_observed,
            Some(RepeatObservation::Result {
                operand: RepeatObservedOperand {
                    name: "dst",
                    field: Some('e'),
                    location: RepeatOperandLocation::EffectiveAddress,
                },
            })
        );
        assert_eq!(
            form("short.pop_sreg_s").attributes.repeat_observed,
            Some(RepeatObservation::Result {
                operand: RepeatObservedOperand {
                    name: "reg",
                    field: Some('s'),
                    location: RepeatOperandLocation::SegmentRegister,
                },
            })
        );
        assert_eq!(form("extrashort.nop").attributes.repeat_observed, None);
    }

    #[test]
    fn every_repcc_form_has_a_runtime_resolvable_observation_target() {
        for generated_form in GENERATED_FORMS {
            if !generated_form.attributes.repeat_repcc {
                assert_eq!(
                    generated_form.attributes.repeat_observed, None,
                    "{} unexpectedly has repeat observation metadata",
                    generated_form.id
                );
                continue;
            }

            let observation = generated_form
                .attributes
                .repeat_observed
                .unwrap_or_else(|| panic!("{} has no repeat observation", generated_form.id));
            let operand = match observation {
                RepeatObservation::Computed => continue,
                RepeatObservation::Result { operand } | RepeatObservation::Source { operand } => {
                    operand
                }
            };
            assert!(
                !operand.name.is_empty(),
                "{} has an empty canonical operand name",
                generated_form.id
            );

            let expected_field = match operand.location {
                RepeatOperandLocation::Rn => Some((FieldKind::Rn, 4)),
                RepeatOperandLocation::EffectiveAddress => Some((FieldKind::Ea7, 7)),
                RepeatOperandLocation::SegmentRegister => Some((FieldKind::Bits, 3)),
                RepeatOperandLocation::StackPointer | RepeatOperandLocation::CodeSegment => None,
            };
            match (operand.field, expected_field) {
                (Some(symbol), Some((kind, width))) => assert!(
                    generated_form.fields.iter().any(|field| {
                        field.symbol == symbol && field.kind == kind && field.width == width
                    }),
                    "{} observation field {symbol:?} has the wrong generated field kind",
                    generated_form.id
                ),
                (None, None) => {}
                _ => panic!(
                    "{} observation location {:?} has incompatible field {:?}",
                    generated_form.id, operand.location, operand.field
                ),
            }
        }
    }

    #[test]
    fn fieldless_repeat_observations_enumerate_only_fixed_architectural_targets() {
        let mut fieldless = GENERATED_FORMS
            .iter()
            .filter_map(|generated_form| {
                let operand = match generated_form.attributes.repeat_observed? {
                    RepeatObservation::Computed => return None,
                    RepeatObservation::Result { operand }
                    | RepeatObservation::Source { operand } => operand,
                };
                operand.field.is_none().then_some((
                    generated_form.id,
                    operand.name,
                    operand.location,
                ))
            })
            .collect::<Vec<_>>();
        fieldless.sort_unstable_by_key(|(id, _, _)| *id);

        assert_eq!(
            fieldless,
            vec![
                (
                    "extrashort.add_q_8_sp",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "extrashort.mov_q_rn_r_sp",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "extrashort.push_cs",
                    "reg",
                    RepeatOperandLocation::CodeSegment,
                ),
                (
                    "extrashort.sub_q_8_sp",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "medium.add_q_ea_sp",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "medium.add_q_ea_sp.2",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "medium.sub_q_ea_sp",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "medium.sub_q_ea_sp.2",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "short.add_q_imm8_i_sp",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
                (
                    "short.sub_q_imm8_i_sp",
                    "dst",
                    RepeatOperandLocation::StackPointer,
                ),
            ]
        );
    }

    #[test]
    fn generated_destination_overlap_relations_retain_operand_fields() {
        let xchg = form("short.xchg_x_rn_s_rn_d");
        assert_eq!(xchg.destination_overlap.len(), 1);
        assert_eq!(xchg.destination_overlap[0].operands, ["lhs", "rhs"]);
        assert_eq!(xchg.destination_overlap[0].operand_fields, ['s', 'd']);
        assert_eq!(
            xchg.destination_overlap[0].rule,
            DestinationOverlapRule::SameValue
        );

        let divmod = form("extralong.divmodu_x_ea_e_rn_q_rn_r");
        assert_eq!(divmod.destination_overlap.len(), 1);
        assert_eq!(
            divmod.destination_overlap[0].operands,
            ["quotient", "remainder"]
        );
        assert_eq!(divmod.destination_overlap[0].operand_fields, ['q', 'r']);
        assert_eq!(
            divmod.destination_overlap[0].rule,
            DestinationOverlapRule::IllegalInstruction
        );

        for generated_form in GENERATED_FORMS {
            for relation in generated_form.destination_overlap {
                for field in relation.operand_fields {
                    assert!(
                        generated_form
                            .fields
                            .iter()
                            .any(|generated| generated.symbol == field),
                        "{} overlap operand field {field:?} is not generated",
                        generated_form.id
                    );
                    assert!(
                        extract_pattern_field(generated_form.pattern, field, generated_form.value)
                            .is_some(),
                        "{} overlap operand field {field:?} is not encoded",
                        generated_form.id
                    );
                }
            }
        }
    }

    #[test]
    fn generated_ea_fields_preserve_form_local_syntax_operand_ordinals() {
        let ea_destination = form("medium.add_x_rn_s_ea_e");
        assert_eq!(ea_destination.ea_fields.len(), 1);
        assert_eq!(ea_destination.ea_fields[0].symbol, 'e');
        assert_eq!(ea_destination.ea_fields[0].syntax_operand_ordinal, 1);

        let ea_source = form("medium.add_x_ea_e_rn_d");
        assert_eq!(ea_source.ea_fields.len(), 1);
        assert_eq!(ea_source.ea_fields[0].symbol, 'e');
        assert_eq!(ea_source.ea_fields[0].syntax_operand_ordinal, 0);

        let after_fieldless_operand = form("medium.add_q_imm64_ea_e");
        assert_eq!(after_fieldless_operand.ea_fields.len(), 1);
        assert_eq!(after_fieldless_operand.ea_fields[0].symbol, 'e');
        assert_eq!(
            after_fieldless_operand.ea_fields[0].syntax_operand_ordinal,
            1
        );

        let two_eas = form("long.cmp_x_ea_s_ea_d");
        assert_eq!(two_eas.ea_fields.len(), 2);
        assert_eq!(two_eas.ea_fields[0].symbol, 's');
        assert_eq!(two_eas.ea_fields[0].syntax_operand_ordinal, 0);
        assert_eq!(two_eas.ea_fields[1].symbol, 'd');
        assert_eq!(two_eas.ea_fields[1].syntax_operand_ordinal, 1);

        for generated_form in GENERATED_FORMS {
            let encoded_ea_fields = generated_form
                .fields
                .iter()
                .filter(|field| field.kind == super::FieldKind::Ea7)
                .count();
            assert_eq!(
                generated_form.ea_fields.len(),
                encoded_ea_fields,
                "{} does not map every EA field",
                generated_form.id
            );
            for (index, ea_field) in generated_form.ea_fields.iter().enumerate() {
                assert!(
                    generated_form
                        .fields
                        .iter()
                        .any(|field| field.symbol == ea_field.symbol
                            && field.kind == super::FieldKind::Ea7),
                    "{} maps unknown EA field {:?}",
                    generated_form.id,
                    ea_field.symbol
                );
                assert!(
                    generated_form.ea_fields[..index]
                        .iter()
                        .all(|prior| prior.symbol != ea_field.symbol),
                    "{} maps EA field {:?} more than once",
                    generated_form.id,
                    ea_field.symbol
                );
            }
        }
    }

    #[test]
    fn direct_tables_match_reference_for_every_small_class_payload() {
        for (class, bits) in [
            (EncodingClass::ExtraShort, 7),
            (EncodingClass::Short, 14),
            (EncodingClass::Medium, 18),
        ] {
            for payload in 0..1u64 << bits {
                assert_eq!(
                    decode_form(class, payload).map(|form| form.form),
                    reference_form(class, payload),
                    "{class:?} payload 0x{payload:x}"
                );
            }
        }
    }

    #[test]
    fn hierarchical_tables_match_reference_for_sampled_large_class_payloads() {
        const { assert!(LONG_LOOKUP_MAX_DEPTH <= 5) };
        const { assert!(EXTRALONG_LOOKUP_MAX_DEPTH <= 6) };
        let mut random = 0x6a09_e667_f3bc_c909u64;
        for (class, bits) in [(EncodingClass::Long, 26), (EncodingClass::ExtraLong, 34)] {
            for _ in 0..20_000 {
                random ^= random << 13;
                random ^= random >> 7;
                random ^= random << 17;
                let payload = random & ((1u64 << bits) - 1);
                assert_eq!(
                    decode_form(class, payload).map(|form| form.form),
                    reference_form(class, payload),
                    "{class:?} payload 0x{payload:x}"
                );
            }
        }
    }

    fn reference_form(class: EncodingClass, payload: u64) -> Option<FormId> {
        GENERATED_FORMS
            .iter()
            .find(|form| form.class == class && form_accepts(form, payload))
            .map(|form| form.form)
    }

    fn form(id: &str) -> &'static super::GeneratedForm {
        GENERATED_FORMS
            .iter()
            .find(|form| form.id == id)
            .unwrap_or_else(|| panic!("missing generated form {id}"))
    }

    fn set_field(pattern: &str, field: char, mut payload: u64, value: u64) -> u64 {
        let positions = pattern
            .chars()
            .enumerate()
            .filter_map(|(index, symbol)| (symbol == field).then_some(pattern.len() - index - 1))
            .collect::<Vec<_>>();
        for (field_index, payload_index) in positions.iter().enumerate() {
            let source_index = positions.len() - field_index - 1;
            let bit = (value >> source_index) & 1;
            payload &= !(1u64 << payload_index);
            payload |= bit << payload_index;
        }
        payload
    }
}
