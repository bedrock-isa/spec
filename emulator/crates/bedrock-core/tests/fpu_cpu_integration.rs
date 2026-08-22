use bedrock_bus::{Bus, Ram};
use bedrock_core::fpu::env::FpCauses;
use bedrock_core::fpu::trans::contracts::{TransOperation, contract_for_operation};
use bedrock_core::{Cpu, EventControl, Flags, Status, StepResult};
use bedrock_isa::{EncodingClass, generated::GENERATED_FORMS};

fn encoded_form(id: &str, fields: &[(char, u64)], appended: &[u8]) -> Vec<u8> {
    let form = GENERATED_FORMS
        .iter()
        .find(|form| form.id == id)
        .unwrap_or_else(|| panic!("missing generated form {id}"));
    let mut payload = form.value;
    for &(symbol, value) in fields {
        let width = form
            .pattern
            .chars()
            .filter(|&field| field == symbol)
            .count();
        assert!(width != 0, "field {symbol} is absent from {id}");
        let mut field_index = 0;
        for (pattern_index, field) in form.pattern.chars().enumerate() {
            if field != symbol {
                continue;
            }
            let payload_bit = form.pattern.len() - pattern_index - 1;
            let value_bit = width - field_index - 1;
            payload &= !(1_u64 << payload_bit);
            payload |= ((value >> value_bit) & 1) << payload_bit;
            field_index += 1;
        }
    }

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
    assert_eq!(bedrock_isa::decode(&bytes).unwrap().allocation_id, id);
    bytes
}

fn append_form(program: &mut Vec<u8>, id: &str, fields: &[(char, u64)], appended: &[u8]) {
    program.extend_from_slice(&encoded_form(id, fields, appended));
}

fn configure_event_entry(cpu: &mut Cpu, epc: u64, fsp: u64) {
    cpu.state_mut().ecr = EventControl::from_raw(1);
    cpu.state_mut().epc = epc;
    cpu.state_mut().fsp = fsp;
}

#[test]
fn base_fpu_commits_results_updates_flags_and_accrues_fflags() {
    let mut program = Vec::new();
    append_form(
        &mut program,
        "medium.fadd_x_fn_s_fn_d",
        &[('z', 0), ('s', 1), ('d', 0)],
        &[],
    );
    append_form(
        &mut program,
        "medium.fdiv_x_fn_s_fn_d",
        &[('z', 1), ('s', 3), ('d', 2)],
        &[],
    );
    append_form(
        &mut program,
        "medium.fcmp_x_fn_s_fn_d",
        &[('z', 1), ('s', 4), ('d', 5)],
        &[],
    );

    let mut ram = Ram::new(program.len());
    ram.load(0, &program).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().f[0] = 0xffff_ffff_3f80_0000;
    cpu.state_mut().f[1] = 0x4000_0000;
    cpu.state_mut().f[2] = 1.0_f64.to_bits();
    cpu.state_mut().f[3] = 0.0_f64.to_bits();
    cpu.state_mut().f[4] = 2.0_f64.to_bits();
    cpu.state_mut().f[5] = 1.0_f64.to_bits();
    cpu.state_mut().flags = Flags::V;
    cpu.state_mut().fflags = FpCauses::NV.bits();

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().f[0], 0x4040_0000);
    assert_eq!(cpu.state().flags, Flags::V);
    assert_eq!(cpu.state().fflags, FpCauses::NV.bits());

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().f[2], f64::INFINITY.to_bits());
    assert_eq!(cpu.state().flags, Flags::V);
    assert_eq!(cpu.state().fflags, FpCauses::NV.union(FpCauses::DZ).bits());

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().flags, Flags::N | Flags::C);
    assert_eq!(cpu.state().fflags, FpCauses::NV.union(FpCauses::DZ).bits());
}

#[test]
fn enabled_fpu_cause_delivers_event_0x0e_before_any_fpu_or_flags_commit() {
    let bytes = encoded_form(
        "medium.fdiv_x_fn_s_fn_d",
        &[('z', 1), ('s', 1), ('d', 0)],
        &[],
    );
    let mut ram = Ram::new(0x2000);
    ram.load(0, &bytes).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = Status::empty();
    configure_event_entry(&mut cpu, 0x100, 0x1000);
    cpu.state_mut().f[0] = 1.0_f64.to_bits();
    cpu.state_mut().f[1] = 0.0_f64.to_bits();
    cpu.state_mut().fstatus = FpCauses::DZ.bits();
    cpu.state_mut().fflags = FpCauses::NV.bits();
    cpu.state_mut().flags = Flags::C | Flags::Z;

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x100);
    assert_eq!(cpu.state().sp, 0xff0);
    assert_eq!(cpu.state().uinfo, 0x0e);
    assert_eq!(cpu.state().upc, 0);
    assert_eq!(cpu.state().f[0], 1.0_f64.to_bits());
    assert_eq!(cpu.state().flags, Flags::C | Flags::Z);
    assert_eq!(cpu.state().fflags, FpCauses::NV.bits());
    assert_eq!(cpu.state().fstatus, FpCauses::DZ.bits());
    assert_eq!(ram.read_u64(0xff0).unwrap(), u64::from(FpCauses::DZ.bits()));
    assert_eq!(ram.read_u64(0xff8).unwrap(), 0);
}

#[test]
fn fptransa_executes_and_cpuid_advertises_extension_and_accuracy_contract() {
    let mut program = Vec::new();
    append_form(
        &mut program,
        "long.fsina_x_fn_s_fn_d",
        &[('z', 1), ('s', 1), ('d', 0)],
        &[],
    );
    append_form(&mut program, "medium.cpuid_rn_r", &[('r', 3)], &[]);
    append_form(&mut program, "medium.cpuid_rn_r", &[('r', 3)], &[]);

    let mut ram = Ram::new(program.len());
    ram.load(0, &program).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().f[0] = u64::MAX;
    cpu.state_mut().f[1] = 0.0_f64.to_bits();

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().f[0], 0.0_f64.to_bits());

    cpu.state_mut().r[3] = (1_u64 << 32) | 1;
    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().r[3], 0b111);

    let contract = contract_for_operation(TransOperation::Sine);
    cpu.state_mut().r[3] = (1_u64 << 32) | (1 << 16) | u64::from(contract.contract_id);
    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().r[3], contract.cpuid_result());
    assert_eq!(contract.cpuid_result(), 0x8000_0001_0100_0100);
}

#[test]
fn save_restore_round_trips_fp_without_touching_the_vector_component() {
    let save = encoded_form("medium.save_ea_e", &[('e', 15)], &[]);
    let restore = encoded_form("medium.restore_ea_e", &[('e', 15)], &[]);
    let restore_pc = save.len() as u64;
    let mut ram = Ram::new(0x2000);
    ram.load(0, &save).unwrap();
    ram.load(restore_pc, &restore).unwrap();
    ram.write_u64(0x1180, 0xfeed_face_cafe_beef).unwrap();

    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().r[0] = 0x1234;
    cpu.state_mut().r[15] = 0x1000;
    cpu.state_mut().f[0] = 1.25_f64.to_bits();
    cpu.state_mut().f[15] = (-2.5_f64).to_bits();
    cpu.state_mut().fflags = FpCauses::NX.bits();
    cpu.state_mut().fstatus = FpCauses::DZ.bits();
    cpu.state_mut().flags = Flags::C | Flags::Z;

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(ram.read_u64(0x1008).unwrap(), 1);
    assert_eq!(ram.read_u64(0x10c0).unwrap(), 1.25_f64.to_bits());
    assert_eq!(ram.read_u64(0x1138).unwrap(), (-2.5_f64).to_bits());
    assert_eq!(
        ram.read_u64(0x1140).unwrap(),
        u64::from(FpCauses::NX.bits())
    );
    assert_eq!(
        ram.read_u64(0x1148).unwrap(),
        u64::from(FpCauses::DZ.bits())
    );
    assert_eq!(ram.read_u64(0x1178).unwrap(), 0);
    assert_eq!(ram.read_u64(0x1180).unwrap(), 0xfeed_face_cafe_beef);

    cpu.state_mut().r[0] = 0;
    cpu.state_mut().f[0] = 0;
    cpu.state_mut().f[15] = 0;
    cpu.state_mut().fflags = 0;
    cpu.state_mut().fstatus = 0;
    cpu.state_mut().flags = Flags::empty();

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().r[0], 0x1234);
    assert_eq!(cpu.state().r[15], 0x1000);
    assert_eq!(cpu.state().f[0], 1.25_f64.to_bits());
    assert_eq!(cpu.state().f[15], (-2.5_f64).to_bits());
    assert_eq!(cpu.state().fflags, FpCauses::NX.bits());
    assert_eq!(cpu.state().fstatus, FpCauses::DZ.bits());
    assert_eq!(cpu.state().flags, Flags::C | Flags::Z);
    assert_eq!(cpu.state().status, Status::PM);
}

#[test]
fn floating_pair_push_and_pop_use_the_architectural_pair_and_word_order() {
    let push = encoded_form("extrashort.fpushp_pair_id_i", &[('i', 4)], &[]);
    let pop = encoded_form("extrashort.fpopp_pair_id_i", &[('i', 4)], &[]);
    let mut ram = Ram::new(0x400);
    ram.load(0, &push).unwrap();
    ram.load(push.len() as u64, &pop).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().sp = 0x300;
    cpu.state_mut().f[8] = 0x8888;
    cpu.state_mut().f[9] = 0x9999;

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().sp, 0x2f0);
    assert_eq!(ram.read_u64(0x2f0).unwrap(), 0x9999);
    assert_eq!(ram.read_u64(0x2f8).unwrap(), 0x8888);

    cpu.state_mut().f[8] = 0;
    cpu.state_mut().f[9] = 0;
    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().sp, 0x300);
    assert_eq!(cpu.state().f[8], 0x8888);
    assert_eq!(cpu.state().f[9], 0x9999);
}

#[test]
fn canonical_generated_fpu_route_uses_the_same_fp_state_and_exceptions() {
    let mut program = Vec::new();
    append_form(
        &mut program,
        "long.fcvtu_x_rn_s_fn_d",
        &[('z', 1), ('s', 0), ('d', 1)],
        &[],
    );
    append_form(
        &mut program,
        "medium.fmul_x_fn_s_fn_d",
        &[('z', 1), ('s', 1), ('d', 0)],
        &[],
    );
    append_form(
        &mut program,
        "medium.fdiv_x_fn_s_fn_d",
        &[('z', 1), ('s', 2), ('d', 0)],
        &[],
    );
    let mut ram = Ram::new(program.len());
    ram.load(0, &program).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().r[0] = 2;
    cpu.state_mut().f[0] = 3.0_f64.to_bits();

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().f[1], 2.0_f64.to_bits());
    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().f[0], 6.0_f64.to_bits());
    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().f[0], f64::INFINITY.to_bits());
    assert_eq!(cpu.state().fflags, FpCauses::DZ.bits());
}
