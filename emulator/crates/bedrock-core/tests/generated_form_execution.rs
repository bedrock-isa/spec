use bedrock_bus::{Bus, Ram};
use bedrock_core::{Cpu, EventControl, StepResult, Trap};
use bedrock_isa::generated::{GENERATED_FORMS, Opcode};
use bedrock_isa::table::{
    DestinationOverlapRule, EncodingClass, FieldKind, GeneratedConstraint, GeneratedForm,
    extract_pattern_field, form_accepts,
};
use bedrock_isa::{CompactEa, DisplacementWidth};
use std::panic::{AssertUnwindSafe, catch_unwind};

const DATA_ADDRESS: u64 = 0x1_0000;
const STACK_ADDRESS: u64 = 0x1_4000;
const EVENT_PC: u64 = 0x1_8000;
const EVENT_STACK: u64 = 0x1_e000;
const RAM_SIZE: usize = 0x2_0000;

fn set_field(pattern: &str, symbol: char, mut payload: u64, value: u64) -> u64 {
    let positions = pattern
        .chars()
        .enumerate()
        .filter_map(|(index, field)| (field == symbol).then_some(pattern.len() - index - 1))
        .collect::<Vec<_>>();
    for (field_index, payload_index) in positions.iter().enumerate() {
        let source_index = positions.len() - field_index - 1;
        payload &= !(1_u64 << payload_index);
        payload |= ((value >> source_index) & 1) << payload_index;
    }
    payload
}

fn representative_payload(form: &GeneratedForm) -> u64 {
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
                        .expect("generated destination constraint must name an EA")
                        .symbol
                } else {
                    field.expect("generated non-destination constraint must name a field")
                };
                payload = set_field(form.pattern, symbol, payload, 0x00);
            }
        }
    }
    assert!(form_accepts(form, payload), "{} baseline", form.id);

    for field in form.fields {
        let preferred: &[u64] = match field.kind {
            FieldKind::Rn => match field.symbol {
                'd' => &[2, 1, 0, 3],
                's' | 'l' => &[1, 2, 0, 3],
                _ => &[1, 2, 0, 3],
            },
            FieldKind::Freg => match field.symbol {
                'd' | 'r' => &[2, 1, 0, 3],
                _ => &[1, 2, 0, 3],
            },
            FieldKind::Ea7 => &[0x00, 0x01, 0x59, 0x5a, 0x5b, 0x58],
            FieldKind::Condition => &[2, 1, 3, 0],
            FieldKind::Size | FieldKind::Bits => &[0, 1, 2, 3, 4],
            FieldKind::Immediate => &[1, 0, 2, 3],
        };
        if let Some(candidate) = preferred.iter().find_map(|value| {
            let candidate = set_field(form.pattern, field.symbol, payload, *value);
            form_accepts(form, candidate).then_some(candidate)
        }) {
            payload = candidate;
        }
    }

    for relation in form
        .destination_overlap
        .iter()
        .filter(|relation| relation.rule == DestinationOverlapRule::IllegalInstruction)
    {
        let [lhs, rhs] = relation.operand_fields;
        let lhs_value =
            extract_pattern_field(form.pattern, lhs, payload).expect("generated overlap lhs field");
        let rhs_value =
            extract_pattern_field(form.pattern, rhs, payload).expect("generated overlap rhs field");
        if lhs_value == rhs_value {
            let lhs_width = form
                .fields
                .iter()
                .find(|field| field.symbol == lhs)
                .expect("generated overlap lhs metadata")
                .width;
            let rhs_width = form
                .fields
                .iter()
                .find(|field| field.symbol == rhs)
                .expect("generated overlap rhs metadata")
                .width;
            payload = (0..1_u64 << lhs_width)
                .find_map(|lhs_value| {
                    (0..1_u64 << rhs_width).find_map(|rhs_value| {
                        if lhs_value == rhs_value {
                            return None;
                        }
                        let candidate = set_field(form.pattern, lhs, payload, lhs_value);
                        let candidate = set_field(form.pattern, rhs, candidate, rhs_value);
                        form_accepts(form, candidate).then_some(candidate)
                    })
                })
                .unwrap_or_else(|| panic!("{} has no non-overlapping representative", form.id));
        }
    }

    assert!(form_accepts(form, payload), "{} preferred", form.id);
    payload
}

fn append_width(bytes: &mut Vec<u8>, width: DisplacementWidth, value: u64) {
    bytes.extend_from_slice(&value.to_le_bytes()[..width.bytes()]);
}

fn appended_operand_bytes(form: &GeneratedForm, payload: u64) -> Vec<u8> {
    let mut appended = Vec::new();
    for field in form.ea_fields {
        let value = extract_pattern_field(form.pattern, field.symbol, payload)
            .expect("generated EA field") as u8;
        match CompactEa::decode_for(field.profile, value) {
            CompactEa::RegisterIndirect(_) | CompactEa::StackIndirect => {}
            CompactEa::RegisterDisplacement { width, .. }
            | CompactEa::StackDisplacement(width)
            | CompactEa::ProgramCounterDisplacement(width) => {
                append_width(&mut appended, width, 0);
            }
            CompactEa::Absolute32 => {
                appended.extend_from_slice(&(DATA_ADDRESS as u32).to_le_bytes())
            }
            CompactEa::Absolute64 => appended.extend_from_slice(&DATA_ADDRESS.to_le_bytes()),
            CompactEa::Immediate(width) => append_width(&mut appended, width, 1),
            CompactEa::FloatImmediate(width) => append_width(&mut appended, width, 0),
            CompactEa::VectorStride { displacement } => {
                appended.push(0x00);
                if let Some(width) = displacement {
                    append_width(&mut appended, width, 0);
                }
            }
            CompactEa::Ext1 { displacement } => {
                appended.push(0x00);
                if let Some(width) = displacement {
                    append_width(&mut appended, width, 0);
                }
            }
            CompactEa::Ext2 { displacement } => {
                appended.extend_from_slice(&[0x80, 0x00]);
                if let Some(width) = displacement {
                    append_width(&mut appended, width, 0);
                }
            }
            CompactEa::Reserved(value) => panic!("{} selected reserved EA {value:#x}", form.id),
        }
    }

    let fixed_start = appended.len();
    for (needle, width, value) in [
        ("<imm8>", 1, 1_u64),
        ("<imm8s>", 1, 1_u64),
        ("<imm16s>", 2, 1_u64),
        ("<imm16>", 2, 1_u64),
        ("<imm16/bitmap>", 2, 1_u64),
        ("<imm32>", 4, 1_u64),
        ("<imm32s>", 4, 1_u64),
        ("<imm64>", 8, 1_u64),
        ("<fconst_id>", 2, 1_u64),
    ] {
        for _ in 0..form.text.match_indices(needle).count() {
            appended.extend_from_slice(&value.to_le_bytes()[..width]);
        }
    }
    assert_eq!(
        usize::from(form.fixed_operand_bytes),
        appended.len() - fixed_start,
        "{} has incorrect fixed operand payload metadata",
        form.id
    );
    appended
}

fn encode(form: &GeneratedForm, payload: u64, appended: &[u8]) -> Vec<u8> {
    let opcode_bytes = form.class.opcode_bytes();
    let length = opcode_bytes + appended.len();
    let mut bytes = Vec::with_capacity(length);
    match form.class {
        EncodingClass::ExtraShort => bytes.push(payload as u8),
        EncodingClass::Short => {
            bytes.push(0x80 | ((payload >> 8) as u8 & 0x3f));
            bytes.push(payload as u8);
        }
        EncodingClass::Medium
        | EncodingClass::Long
        | EncodingClass::ExtraLong
        | EncodingClass::Xxlong => {
            assert!((opcode_bytes..=18).contains(&length), "{} length", form.id);
            bytes.push(
                0xc0 | (((length - 3) as u8) << 2)
                    | ((payload >> ((opcode_bytes - 1) * 8)) as u8 & 3),
            );
            for index in (0..opcode_bytes - 1).rev() {
                bytes.push((payload >> (index * 8)) as u8);
            }
        }
    }
    bytes.extend_from_slice(appended);
    assert_eq!(bytes.len(), length, "{} framing", form.id);
    bytes
}

fn execute_one(form: &GeneratedForm, bytes: &[u8]) -> Option<String> {
    let mut ram = Ram::new(RAM_SIZE);
    ram.load(0, bytes).expect("instruction fits in RAM");
    let mut body = [0x01; 64];
    body[0] = 0x60;
    ram.load(bytes.len() as u64, &body)
        .expect("trailing NOP/group body fits in RAM");
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().ecr = EventControl::from_raw(1);
    cpu.state_mut().epc = EVENT_PC;
    cpu.state_mut().fsp = EVENT_STACK;
    cpu.state_mut().sp = STACK_ADDRESS;
    cpu.state_mut().r.fill(1);
    cpu.state_mut().r[0] = DATA_ADDRESS;
    cpu.state_mut().f.fill(1.0_f64.to_bits());

    let result = match catch_unwind(AssertUnwindSafe(|| cpu.step(&mut ram))) {
        Ok(result) => result,
        Err(_) => return Some(format!("{} panicked during Cpu::step", form.id)),
    };
    if form.opcode == Opcode::Illegal {
        if cpu.state().pc != EVENT_PC {
            return Some(format!(
                "{} explicit ILLEGAL did not deliver event: {result:?}",
                form.id
            ));
        }
        let event = ram.read_u64(cpu.state().sp + 8).ok();
        if event != Some(0x03) {
            return Some(format!("{} explicit ILLEGAL event was {event:?}", form.id));
        }
        return None;
    }

    if let StepResult::Trap(Trap::IllegalInstruction { cause, .. }) = &result {
        return Some(format!("{} trapped IllegalInstruction::{cause:?}", form.id));
    }
    if cpu.state().pc == EVENT_PC {
        let event = ram.read_u64(cpu.state().sp + 8).ok();
        if event == Some(0x03) {
            return Some(format!("{} delivered architectural event 0x03", form.id));
        }
    }
    None
}

#[test]
fn every_generated_form_decodes_and_reaches_a_non_illegal_execution_path() {
    let mut offenders = Vec::new();
    for form in GENERATED_FORMS {
        let payload = representative_payload(form);
        let appended = appended_operand_bytes(form, payload);
        let bytes = encode(form, payload, &appended);
        let decoded = bedrock_isa::decode(&bytes)
            .unwrap_or_else(|error| panic!("{} public decode failed: {error}", form.id));
        assert_eq!(
            usize::from(decoded.length_bytes),
            bytes.len(),
            "{}",
            form.id
        );
        assert_eq!(decoded.form, form.form, "{}", form.id);
        assert!(
            std::ptr::eq(decoded.generated_form, form),
            "{} retained a different generated form",
            form.id
        );
        assert_eq!(decoded.allocation_id, form.id, "{}", form.id);
        assert_eq!(decoded.opcode, form.opcode, "{}", form.id);
        if let Some(offender) = execute_one(form, &bytes) {
            offenders.push(offender);
        }
    }
    assert!(
        offenders.is_empty(),
        "non-ILLEGAL generated forms reached ILLEGAL paths:\n{}",
        offenders.join("\n")
    );
}
