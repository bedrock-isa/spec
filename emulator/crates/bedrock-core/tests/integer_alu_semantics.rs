use bedrock_bus::{Bus, Ram};
use bedrock_core::{Cpu, EventControl, Flags, PageTableControl, StepResult};
use bedrock_isa::{generated::GENERATED_FORMS, EncodingClass};

const PTE_P: u64 = 1 << 0;
const PTE_W: u64 = 1 << 1;
const PTE_X: u64 = 1 << 2;
const PTE_U: u64 = 1 << 3;
const PTE_T: u64 = 1 << 11;

const WIDTHS: [(u64, u32, u64); 4] = [
    (0, 8, 0xff),
    (1, 16, 0xffff),
    (2, 32, 0xffff_ffff),
    (3, 64, u64::MAX),
];

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
        assert!(
            width == 64 || value < 1_u64 << width,
            "field {symbol} overflow"
        );
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
        EncodingClass::Medium | EncodingClass::Long | EncodingClass::ExtraLong => {
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

fn register_value(upper: u64, mask: u64, selected: u64) -> u64 {
    (upper & !mask) | (selected & mask)
}

fn run_register_instruction(bytes: &[u8], registers: &[(usize, u64)], flags: Flags) -> Cpu {
    let mut ram = Ram::new(0x100);
    ram.load(0, bytes).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    for &(register, value) in registers {
        cpu.state_mut().r[register] = value;
    }
    cpu.state_mut().flags = flags;
    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, bytes.len() as u64);
    cpu
}

#[test]
fn mov_and_extsq_define_complete_sub_quad_register_results() {
    for (id, fields, source, expected) in [
        (
            "short.mov_b_rn_s_rn_d",
            vec![('s', 1), ('d', 2)],
            0x1122_3344_5566_7780,
            0x80,
        ),
        (
            "short.mov_w_rn_s_rn_d",
            vec![('s', 1), ('d', 2)],
            0x1122_3344_5566_8001,
            0x8001,
        ),
        (
            "short.mov_x_rn_s_rn_d",
            vec![('z', 0), ('s', 1), ('d', 2)],
            0x1122_3344_8000_0001,
            0x8000_0001,
        ),
        (
            "medium.extsq_b_rn_s_rn_d",
            vec![('s', 1), ('d', 2)],
            0x1122_3344_5566_7780,
            0xffff_ffff_ffff_ff80,
        ),
        (
            "medium.extsq_w_rn_s_rn_d",
            vec![('s', 1), ('d', 2)],
            0x1122_3344_5566_8001,
            0xffff_ffff_ffff_8001,
        ),
        (
            "short.extsq_l_rn_s_rn_d",
            vec![('s', 1), ('d', 2)],
            0x1122_3344_8000_0001,
            0xffff_ffff_8000_0001,
        ),
    ] {
        let bytes = encoded_form(id, &fields, &[]);
        let cpu = run_register_instruction(
            &bytes,
            &[(1, source), (2, 0xaabb_ccdd_eeff_0011)],
            Flags::all(),
        );
        assert_eq!(cpu.state().r[2], expected, "{id}");
        assert_eq!(cpu.state().flags, Flags::all(), "{id}");
    }
}

#[test]
fn zero_effective_count_still_canonicalizes_shift_and_rotate_register_results() {
    for (id, expected) in [
        ("short.shl_x_rn_s_rn_d", 0x0000_0000_8000_0001),
        ("short.shr_x_rn_s_rn_d", 0x0000_0000_8000_0001),
        ("short.rol_x_rn_s_rn_d", 0x0000_0000_8000_0001),
        ("short.ror_x_rn_s_rn_d", 0x0000_0000_8000_0001),
        ("short.sar_x_rn_s_rn_d", 0xffff_ffff_8000_0001),
    ] {
        let bytes = encoded_form(id, &[('z', 0), ('s', 1), ('d', 2)], &[]);
        let cpu =
            run_register_instruction(&bytes, &[(1, 32), (2, 0x1122_3344_8000_0001)], Flags::all());
        assert_eq!(cpu.state().r[2], expected, "{id}");
        assert_eq!(cpu.state().flags, Flags::all(), "{id}");
    }
}

fn expected_extract(high: u64, low: u64, bits: u32, mask: u64, offset: u32) -> u64 {
    if offset >= bits * 2 {
        0
    } else {
        let concatenated = (u128::from(high & mask) << bits) | u128::from(low & mask);
        (concatenated >> offset) as u64 & mask
    }
}

fn install_four_level_root(ram: &mut Ram) {
    let table_flags = PTE_P | PTE_W | PTE_X | PTE_U | PTE_T;
    ram.write_u64(0x1000, 0x2000 | table_flags).unwrap();
    ram.write_u64(0x2000, 0x3000 | table_flags).unwrap();
    ram.write_u64(0x3000, 0x4000 | table_flags).unwrap();
}

fn map_low_page(ram: &mut Ram, virtual_page: u64, physical_page: u64, flags: u64) {
    ram.write_u64(0x4000 + virtual_page * 8, physical_page | PTE_P | flags)
        .unwrap();
}

fn paged_fault_fixture(bytes: &[u8], map_data_read_only: bool) -> (Cpu, Ram) {
    let mut ram = Ram::new(0x20_000);
    install_four_level_root(&mut ram);
    map_low_page(&mut ram, 0, 0x8000, PTE_X | PTE_U);
    if map_data_read_only {
        map_low_page(&mut ram, 1, 0x9000, PTE_U);
    }
    map_low_page(&mut ram, 5, 0xd000, PTE_X);
    map_low_page(&mut ram, 6, 0xe000, PTE_W);
    ram.load(0x8000, bytes).unwrap();

    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
    cpu.state_mut().ecr = EventControl::from_raw(1);
    cpu.state_mut().epc = 0x5000;
    cpu.state_mut().fsp = 0x7000;
    (cpu, ram)
}

#[test]
fn parity_immediates_write_odd_even_selected_width_results_and_preserve_flags() {
    let initial_flags = Flags::V | Flags::C | Flags::N | Flags::Z;
    for (selector, bits, mask) in WIDTHS {
        for (selected_source, expected) in [(1, 1), (3, 0)] {
            let source = register_value(0xf0e1_d2c3_b4a5_9687, mask, selected_source);
            let source_bytes = source.to_le_bytes();
            let bytes = encoded_form(
                "long.parity_x_ea_e_rn_d",
                &[('z', selector), ('e', 0x5b + selector), ('d', 2)],
                &source_bytes[..(bits / 8) as usize],
            );
            let destination = 0xa1b2_c3d4_e5f6_7788;
            let cpu = run_register_instruction(&bytes, &[(2, destination)], initial_flags);
            assert_eq!(
                cpu.state().r[2],
                expected & mask,
                "PARITY width {bits}, source {selected_source:#x}"
            );
            assert_eq!(cpu.state().flags, initial_flags, "PARITY width {bits}");
        }
    }
}

#[test]
fn parity_at0_source_fault_rolls_back_destination_flags_and_pc_effects() {
    let bytes = encoded_form(
        "long.parity_x_ea_e_rn_d",
        &[('z', 3), ('e', 0x00), ('d', 2)],
        &[],
    );
    let (mut cpu, mut ram) = paged_fault_fixture(&bytes, false);
    let destination = 0xfeed_face_cafe_beef;
    let flags = Flags::V | Flags::C | Flags::N | Flags::Z;
    cpu.state_mut().r[0] = 0x1000;
    cpu.state_mut().r[2] = destination;
    cpu.state_mut().flags = flags;

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().r[2], destination);
    assert_eq!(cpu.state().flags, flags);
    assert_eq!(cpu.state().pc, 0x5000);
    assert_eq!(ram.read_u64(0xefa0 + 24).unwrap(), 0);
}

#[test]
fn extract_uses_the_full_concatenation_and_unsigned_imm7_range() {
    let flags = Flags::V | Flags::C | Flags::N | Flags::Z;
    for (selector, bits, mask) in WIDTHS {
        let high = register_value(0x9123_4567_89ab_cdef, mask, 0xa53c_96e1_5a3c_96e1);
        let low = register_value(0x6fed_cba9_7654_3210, mask, 0x3c5a_e196_3c5a_e196);
        let mut offsets = vec![0, bits - 1, bits, bits * 2 - 1];
        if bits * 2 <= 127 {
            offsets.push(bits * 2);
        }
        if !offsets.contains(&127) {
            offsets.push(127);
        }

        for offset in offsets {
            let bytes = encoded_form(
                "extralong.extract_x_imm7_i_rn_h_rn_l",
                &[
                    ('z', selector),
                    ('i', u64::from(offset)),
                    ('h', 1),
                    ('l', 2),
                ],
                &[],
            );
            let cpu = run_register_instruction(&bytes, &[(1, high), (2, low)], flags);
            let selected = expected_extract(high, low, bits, mask, offset);
            assert_eq!(
                cpu.state().r[2],
                selected,
                "EXTRACT width {bits}, offset {offset}"
            );
            assert_eq!(cpu.state().r[1], high, "EXTRACT high width {bits}");
            assert_eq!(cpu.state().flags, flags, "EXTRACT width {bits}");
        }
    }
}

#[test]
fn extract_aliases_high_and_low_from_the_prewrite_value() {
    let flags = Flags::V | Flags::N;
    for (selector, bits, mask) in WIDTHS {
        let value = register_value(0xd1e2_f304_1526_3748, mask, 0x81c3_5aa5_81c3_5aa5);
        let offset = bits - 1;
        let bytes = encoded_form(
            "extralong.extract_x_imm7_i_rn_h_rn_l",
            &[
                ('z', selector),
                ('i', u64::from(offset)),
                ('h', 2),
                ('l', 2),
            ],
            &[],
        );
        let cpu = run_register_instruction(&bytes, &[(2, value)], flags);
        let selected = expected_extract(value, value, bits, mask, offset);
        assert_eq!(cpu.state().r[2], selected, "aliased EXTRACT width {bits}");
        assert_eq!(cpu.state().flags, flags);
    }
}

fn run_carry_register(id: &str, selector: u64, source: u64, destination: u64, flags: Flags) -> Cpu {
    let bytes = encoded_form(id, &[('z', selector), ('s', 1), ('d', 2)], &[]);
    run_register_instruction(&bytes, &[(1, source), (2, destination)], flags)
}

#[test]
fn adc_and_sbb_include_incoming_c_in_full_width_carry_and_borrow() {
    for (selector, bits, mask) in WIDTHS {
        let source = register_value(0x1357_9bdf_2468_ace0, mask, mask);
        let destination = register_value(0xa5a5_5a5a_c3c3_3c3c, mask, 0);
        for (id, incoming, result, expected_flags) in [
            ("medium.adc_x_rn_s_rn_d", false, mask, Flags::N),
            ("medium.adc_x_rn_s_rn_d", true, 0, Flags::C | Flags::Z),
            ("medium.sbb_x_rn_s_rn_d", false, 1, Flags::C),
            ("medium.sbb_x_rn_s_rn_d", true, 0, Flags::C | Flags::Z),
        ] {
            let input_flags = if incoming { Flags::C } else { Flags::empty() };
            let cpu = run_carry_register(id, selector, source, destination, input_flags);
            assert_eq!(
                cpu.state().r[2],
                result & mask,
                "{id} width {bits}, incoming C {incoming}"
            );
            assert_eq!(
                cpu.state().flags,
                expected_flags,
                "{id} width {bits}, incoming C {incoming}"
            );
        }
    }
}

#[test]
fn adc_and_sbb_set_c_for_either_constituent_carry_or_borrow() {
    for (selector, bits, mask) in WIDTHS {
        let adc_source = register_value(0x1357_9bdf_2468_ace0, mask, 1);
        let adc_destination = register_value(0xa5a5_5a5a_c3c3_3c3c, mask, mask);
        let adc = run_carry_register(
            "medium.adc_x_rn_s_rn_d",
            selector,
            adc_source,
            adc_destination,
            Flags::empty(),
        );
        assert_eq!(adc.state().r[2], 0, "ADC first carry width {bits}");
        assert_eq!(adc.state().flags, Flags::C | Flags::Z);

        let sbb_source = register_value(0x1357_9bdf_2468_ace0, mask, 0);
        let sbb_destination = register_value(0xa5a5_5a5a_c3c3_3c3c, mask, 0);
        let sbb = run_carry_register(
            "medium.sbb_x_rn_s_rn_d",
            selector,
            sbb_source,
            sbb_destination,
            Flags::C,
        );
        assert_eq!(sbb.state().r[2], mask, "SBB carry-in borrow width {bits}");
        assert_eq!(sbb.state().flags, Flags::C | Flags::N);
    }
}

#[test]
fn adc_and_sbb_detect_signed_overflow_from_the_complete_operation() {
    for (selector, bits, mask) in WIDTHS {
        let sign = 1_u64 << (bits - 1);
        for (id, selected_destination, result, expected_flags) in [
            (
                "medium.adc_x_rn_s_rn_d",
                sign - 1,
                sign,
                Flags::N | Flags::V,
            ),
            ("medium.sbb_x_rn_s_rn_d", sign, sign - 1, Flags::V),
        ] {
            let source = register_value(0x0123_4567_89ab_cdef, mask, 0);
            let destination = register_value(0xfedc_ba98_7654_3210, mask, selected_destination);
            let cpu = run_carry_register(id, selector, source, destination, Flags::C);
            assert_eq!(
                cpu.state().r[2],
                result & mask,
                "{id} overflow width {bits}"
            );
            assert_eq!(cpu.state().flags, expected_flags, "{id} width {bits}");
        }
    }
}

#[test]
fn adc_and_sbb_at0_destination_faults_roll_back_data_flags_and_pc_effects() {
    for id in ["long.adc_x_rn_s_ea_e", "long.sbb_x_rn_s_ea_e"] {
        let bytes = encoded_form(id, &[('z', 3), ('s', 1), ('e', 0x00)], &[]);
        let (mut cpu, mut ram) = paged_fault_fixture(&bytes, true);
        let destination = 0x7fff_ffff_ffff_ffff;
        let flags = Flags::C | Flags::N;
        ram.write_u64(0x9000, destination).unwrap();
        cpu.state_mut().r[0] = 0x1000;
        cpu.state_mut().r[1] = 1;
        cpu.state_mut().flags = flags;

        assert_eq!(cpu.step(&mut ram), StepResult::Running, "{id}");
        assert_eq!(ram.read_u64(0x9000).unwrap(), destination, "{id}");
        assert_eq!(cpu.state().r[0], 0x1000, "{id}");
        assert_eq!(cpu.state().r[1], 1, "{id}");
        assert_eq!(cpu.state().flags, flags, "{id}");
        assert_eq!(cpu.state().pc, 0x5000, "{id}");
        assert_eq!(ram.read_u64(0xefa0 + 24).unwrap(), 0, "{id}");
    }
}
