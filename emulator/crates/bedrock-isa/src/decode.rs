use crate::generated::{FormId, decode_form};
use crate::header::{HeaderError, InstructionHeader, decode_header, opcode_payload};
use crate::table::{FieldKind, GeneratedForm, extract_pattern_field};
use crate::{CompactEa, DecodedOperand, ExtendedDescriptor, InstructionAttributes, Opcode};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DecodedField {
    pub symbol: char,
    pub kind: FieldKind,
    pub value: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DecodedInstruction {
    pub header: InstructionHeader,
    pub length_bytes: u8,
    pub form: FormId,
    pub generated_form: &'static GeneratedForm,
    pub allocation_id: &'static str,
    pub form_text: &'static str,
    pub opcode: Opcode,
    pub operands: Vec<DecodedOperand>,
    pub fields: Vec<DecodedField>,
    pub attributes: InstructionAttributes,
    pub bytes: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum DecodeError {
    #[error(transparent)]
    Header(#[from] HeaderError),
    #[error("instruction requires {needed} bytes, but only {available} are available")]
    Truncated { needed: usize, available: usize },
    #[error("opcode is reserved or noncanonical")]
    Reserved,
    #[error("instruction uses reserved effective-address encoding 0x{0:02x}")]
    ReservedEffectiveAddress(u8),
    #[error("instruction operand payload needs {needed} bytes, but record has {available}")]
    OperandPayload { needed: usize, available: usize },
}

pub fn decode(bytes: &[u8]) -> Result<DecodedInstruction, DecodeError> {
    let header = decode_header(bytes)?;
    if bytes.len() < usize::from(header.length_bytes) {
        return Err(DecodeError::Truncated {
            needed: usize::from(header.length_bytes),
            available: bytes.len(),
        });
    }
    let record = &bytes[..usize::from(header.length_bytes)];
    let payload = opcode_payload(header, record).ok_or(DecodeError::Truncated {
        needed: usize::from(header.opcode_bytes),
        available: record.len(),
    })?;

    let form = decode_form(header.class, payload).ok_or(DecodeError::Reserved)?;

    let fields = form
        .fields
        .iter()
        .map(|field| DecodedField {
            symbol: field.symbol,
            kind: field.kind,
            value: extract_pattern_field(form.pattern, field.symbol, payload)
                .expect("generated field must occur in pattern"),
        })
        .collect::<Vec<_>>();
    let operands = fields
        .iter()
        .map(lower_field)
        .collect::<Result<Vec<_>, _>>()?;
    validate_operand_payload(form, &fields, header, record)?;
    let attributes = InstructionAttributes {
        instruction_set: form.attributes.instruction_set,
        privileged: form.attributes.privileged,
        repeat_rep: form.attributes.repeat_rep,
        repeat_repcc: form.attributes.repeat_repcc,
        repeat_repg: form.attributes.repeat_repg,
        repeat_observed: form.attributes.repeat_observed,
        flags: form.attributes.flags,
    };

    Ok(DecodedInstruction {
        header,
        length_bytes: header.length_bytes,
        form: form.form,
        generated_form: form,
        allocation_id: form.id,
        form_text: form.text,
        opcode: form.opcode,
        operands,
        fields,
        attributes,
        bytes: record.to_vec(),
    })
}

fn validate_operand_payload(
    form: &GeneratedForm,
    fields: &[DecodedField],
    header: InstructionHeader,
    record: &[u8],
) -> Result<(), DecodeError> {
    let mut cursor = usize::from(header.opcode_bytes);
    for generated in form
        .fields
        .iter()
        .filter(|field| field.kind == FieldKind::Ea7)
    {
        let value = fields
            .iter()
            .find(|field| field.symbol == generated.symbol)
            .expect("generated EA field")
            .value as u8;
        match CompactEa::decode(value) {
            CompactEa::Reserved(value) => return Err(DecodeError::ReservedEffectiveAddress(value)),
            ea @ (CompactEa::Ext1 { .. } | CompactEa::Ext2 { .. }) => {
                let descriptor_bytes = ea.descriptor_bytes();
                let descriptor_payload = record.get(cursor..cursor + descriptor_bytes).ok_or(
                    DecodeError::OperandPayload {
                        needed: cursor + descriptor_bytes,
                        available: record.len(),
                    },
                )?;
                let valid = match ea {
                    CompactEa::Ext1 { .. } => {
                        ExtendedDescriptor::decode_ext1(descriptor_payload).is_some()
                    }
                    CompactEa::Ext2 { .. } => {
                        ExtendedDescriptor::decode_ext2(descriptor_payload).is_some()
                    }
                    _ => false,
                };
                if !valid {
                    return Err(DecodeError::OperandPayload {
                        needed: cursor + descriptor_bytes,
                        available: record.len(),
                    });
                }
                cursor += ea.appended_bytes();
            }
            ea => cursor += ea.appended_bytes(),
        }
    }
    cursor += usize::from(form.fixed_operand_bytes);
    if cursor > record.len() {
        return Err(DecodeError::OperandPayload {
            needed: cursor,
            available: record.len(),
        });
    }
    Ok(())
}

fn lower_field(field: &DecodedField) -> Result<DecodedOperand, DecodeError> {
    Ok(match field.kind {
        FieldKind::Rn => DecodedOperand::Register(field.value as u8),
        FieldKind::Freg => DecodedOperand::FloatingRegister(field.value as u8),
        FieldKind::Ea7 => {
            let ea = CompactEa::decode(field.value as u8);
            if let CompactEa::Reserved(value) = ea {
                return Err(DecodeError::ReservedEffectiveAddress(value));
            }
            DecodedOperand::EffectiveAddress(ea)
        }
        FieldKind::Condition => DecodedOperand::Condition(field.value as u8),
        FieldKind::Size => DecodedOperand::SizeSelector(field.value as u8),
        FieldKind::Immediate => DecodedOperand::Immediate(field.value),
        FieldKind::Bits => DecodedOperand::Bits {
            kind: FieldKind::Bits,
            value: field.value,
        },
    })
}

#[cfg(test)]
mod tests {
    use super::{DecodeError, decode};
    use crate::generated::GENERATED_FORMS;
    use crate::table::GeneratedForm;
    use crate::{
        EncodingClass, Opcode, RepeatObservation, RepeatObservedOperand, RepeatOperandLocation,
    };

    #[test]
    fn decodes_every_extrashort_fixed_and_register_form() {
        assert_eq!(decode(&[0x01]).unwrap().opcode, Opcode::Nop);
        assert_eq!(decode(&[0x32]).unwrap().opcode, Opcode::Push);
    }

    #[test]
    fn decodes_push_cs_extrashort_opcode() {
        let instruction = decode(&[0x0d]).unwrap();
        assert_eq!(instruction.opcode, Opcode::Push);
        assert_eq!(instruction.allocation_id, "extrashort.push_cs");
        assert_eq!(
            instruction.attributes.repeat_observed,
            Some(RepeatObservation::Source {
                operand: RepeatObservedOperand {
                    name: "reg",
                    field: None,
                    location: RepeatOperandLocation::CodeSegment,
                },
            })
        );
    }

    #[test]
    fn reports_truncated_short_instruction() {
        assert!(matches!(
            decode(&[0x80]),
            Err(DecodeError::Truncated {
                needed: 2,
                available: 1
            })
        ));
    }

    #[test]
    fn decodes_all_register_bits_in_short_forms() {
        let mov = decode(&[0x81, 0x90]).unwrap();
        assert_eq!(
            mov.fields
                .iter()
                .find(|field| field.symbol == 's')
                .unwrap()
                .value,
            9
        );
        assert_eq!(
            mov.fields
                .iter()
                .find(|field| field.symbol == 'd')
                .unwrap()
                .value,
            0
        );

        let inc = decode(&[0xa8, 0x0b]).unwrap();
        assert_eq!(
            inc.fields
                .iter()
                .find(|field| field.symbol == 'r')
                .unwrap()
                .value,
            11
        );
    }

    #[test]
    fn imm64_requires_all_eight_trailing_bytes() {
        let form = generated_form("medium.add_q_imm64_ea_e");
        let payload = set_field(form.pattern, 'e', form.value, 0x00);

        assert_eq!(
            decode(&extended_record(form, payload, 10)),
            Err(DecodeError::OperandPayload {
                needed: 11,
                available: 10,
            })
        );
        assert_eq!(
            decode(&extended_record(form, payload, 11))
                .unwrap()
                .allocation_id,
            form.id
        );
    }

    #[test]
    fn fconst_id_requires_both_trailing_bytes() {
        let form = generated_form("medium.fmovcr_x_imm16_fn_d");

        assert_eq!(
            decode(&extended_record(form, form.value, 4)),
            Err(DecodeError::OperandPayload {
                needed: 5,
                available: 4,
            })
        );
        assert_eq!(
            decode(&extended_record(form, form.value, 5))
                .unwrap()
                .allocation_id,
            form.id
        );
    }

    #[test]
    fn repg_requires_its_fieldless_body_length_operand() {
        let form = generated_form("medium.repg_rn_r_ea");

        assert_eq!(
            decode(&extended_record(form, form.value, 4)),
            Err(DecodeError::OperandPayload {
                needed: 5,
                available: 4,
            })
        );
        assert_eq!(
            decode(&extended_record(form, form.value, 5))
                .unwrap()
                .allocation_id,
            form.id
        );
    }

    #[test]
    fn extended_ea_family_fixes_descriptor_and_required_record_lengths() {
        let form = generated_form("medium.inc_x_ea.2");
        let opcode_bytes = form.class.opcode_bytes();

        let ext1_payload = set_field(form.pattern, 'e', form.value, 0x63);
        assert_eq!(
            decode(&extended_record(form, ext1_payload, opcode_bytes)),
            Err(DecodeError::OperandPayload {
                needed: opcode_bytes + 1,
                available: opcode_bytes,
            })
        );
        assert!(decode(&extended_record(form, ext1_payload, opcode_bytes + 1)).is_ok());

        let ext2_payload = set_field(form.pattern, 'e', form.value, 0x68);
        let mut truncated_ext2 = extended_record(form, ext2_payload, opcode_bytes + 1);
        truncated_ext2[opcode_bytes] = 0x80;
        assert_eq!(
            decode(&truncated_ext2),
            Err(DecodeError::OperandPayload {
                needed: opcode_bytes + 2,
                available: opcode_bytes + 1,
            })
        );
        let mut complete_ext2 = extended_record(form, ext2_payload, opcode_bytes + 2);
        complete_ext2[opcode_bytes..].copy_from_slice(&[0x80, 0x00]);
        assert!(decode(&complete_ext2).is_ok());

        let mut old_ambiguous_encoding = extended_record(form, ext1_payload, opcode_bytes + 2);
        old_ambiguous_encoding[opcode_bytes..].copy_from_slice(&[0x92, 0x02]);
        assert!(matches!(
            decode(&old_ambiguous_encoding),
            Err(DecodeError::OperandPayload { .. })
        ));
    }

    fn generated_form(id: &str) -> &'static GeneratedForm {
        GENERATED_FORMS
            .iter()
            .find(|form| form.id == id)
            .unwrap_or_else(|| panic!("missing generated form {id}"))
    }

    fn extended_record(form: &GeneratedForm, payload: u64, length: usize) -> Vec<u8> {
        assert!(matches!(
            form.class,
            EncodingClass::Medium | EncodingClass::Long | EncodingClass::ExtraLong
        ));
        assert!((form.class.opcode_bytes()..=18).contains(&length));
        let opcode_bytes = form.class.opcode_bytes();
        let mut record = vec![0; length];
        record[0] = 0xc0
            | (((length - 3) as u8) << 2)
            | ((payload >> ((opcode_bytes - 1) * 8)) & 0x03) as u8;
        for (index, byte) in record[1..opcode_bytes].iter_mut().enumerate() {
            let shift = (opcode_bytes - index - 2) * 8;
            *byte = (payload >> shift) as u8;
        }
        record
    }

    fn set_field(pattern: &str, symbol: char, mut payload: u64, value: u64) -> u64 {
        let positions = pattern
            .chars()
            .enumerate()
            .filter_map(|(index, field)| (field == symbol).then_some(pattern.len() - index - 1))
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
