use bedrock_bus::{Bus, Ram};
use bedrock_core::{
    AddressSpaceControl, Cpu, EventControl, PageFaultReason, PageTableControl, Status, StepResult,
};

const PTE_P: u64 = 1 << 0;
const PTE_T: u64 = 1 << 1;
const PTE_U: u64 = 1 << 5;
const PTE_W: u64 = 1 << 62;
const PTE_X: u64 = 1 << 63;

fn configure_event_entry(cpu: &mut Cpu, epc: u64, fsp: u64) {
    cpu.state_mut().ecr = EventControl::from_raw(1);
    cpu.state_mut().epc = epc;
    cpu.state_mut().fsp = fsp;
}

fn install_four_level_root(ram: &mut Ram) {
    let table_flags = PTE_P | PTE_T | (1 << 2) | (1 << 3) | (1 << 4) | PTE_U;
    ram.write_u64(0x1000, 0x2000 | table_flags).unwrap();
    ram.write_u64(0x2000, 0x3000 | table_flags).unwrap();
    ram.write_u64(0x3000, 0x4000 | table_flags).unwrap();
}

fn map_low_page(ram: &mut Ram, virtual_page: u64, physical_page: u64, flags: u64) {
    let am = if flags & PTE_X != 0 {
        0b100 << 2
    } else if flags & PTE_W != 0 {
        0b011 << 2
    } else {
        0
    };
    ram.write_u64(
        0x4000 + virtual_page * 8,
        physical_page | PTE_P | (flags & PTE_U) | am,
    )
    .unwrap();
}

#[test]
fn illegal_instruction_delivers_typed_error_frame_with_zero_padding() {
    let mut ram = Ram::new(0x2000);
    ram.write_u8(0, 0x00).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = Status::empty();
    configure_event_entry(&mut cpu, 0x100, 0x1000);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x100);
    assert_eq!(cpu.state().sp, 0xff0);
    assert_eq!(cpu.state().uinfo, 0x03);
    assert_eq!(ram.read_u64(0xff0).unwrap(), 4);
    assert_eq!(ram.read_u64(0xff8).unwrap(), 0);
}

#[test]
fn debug_trace_commits_the_unit_then_saves_the_next_boundary() {
    let mut ram = Ram::new(0x2000);
    ram.write_u8(0, 0x01).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = Status::empty();
    cpu.state_mut().status.insert(Status::TF);
    configure_event_entry(&mut cpu, 0x100, 0x1000);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x100);
    assert_eq!(cpu.state().sp, 0x1000);
    assert_eq!(cpu.state().uinfo, 0);
    assert_eq!(cpu.state().upc, 1);
    assert!(!cpu.state().status.contains(Status::TF));
}

#[test]
fn malformed_eret_frame_delivers_invalid_control_without_consuming_it() {
    let mut ram = Ram::new(0x3000);
    ram.write_u8(0, 0x04).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = (Status::PM | Status::EA).with_event_state(1, false);
    cpu.state_mut().sp = 0x1000;
    configure_event_entry(&mut cpu, 0x200, 0x1800);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x200);
    assert_eq!(cpu.state().sp, 0xfb0);
    assert_eq!(cpu.state().status.event_depth(), 2);
    assert_eq!(ram.read_u64(0xfb8).unwrap(), 0x0d);
    assert_eq!(ram.read_u64(0xfc0).unwrap(), 0);
    assert_eq!(ram.read_u64(0xfc8).unwrap(), 0x1000);
    assert_eq!(ram.read_u64(0xfe8).unwrap(), 0);
    assert_eq!(ram.read_u64(0xff0).unwrap(), 2);
    assert_eq!(ram.read_u64(0xff8).unwrap(), 0);
    assert_eq!(ram.read_u64(0x1000).unwrap(), 0);
}

#[test]
fn page_fault_populates_its_frame_and_eret_restores_the_saved_state() {
    let mut ram = Ram::new(0x20_000);
    install_four_level_root(&mut ram);
    map_low_page(&mut ram, 0, 0x8000, PTE_X | PTE_U);
    map_low_page(&mut ram, 5, 0xd000, PTE_X);
    map_low_page(&mut ram, 6, 0xe000, PTE_W);
    ram.load(0x8000, &[0xc1, 0x18, 0x80]).unwrap();
    ram.write_u8(0xd000, 0x04).unwrap();

    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = Status::empty();
    cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
    cpu.state_mut().ascr = AddressSpaceControl::from_raw(0x1234_0001);
    configure_event_entry(&mut cpu, 0x5000, 0x7000);
    cpu.state_mut().r[0] = 0x1000;
    cpu.state_mut().r[1] = 0xfeed_face;

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x5000);
    assert_eq!(cpu.state().sp, 0x6fe0);
    assert!(cpu.state().status.contains(Status::PM | Status::EA));
    assert_eq!(cpu.state().r[1], 0xfeed_face);

    let frame = 0xefe0;
    assert_eq!(cpu.state().uinfo, 9);
    assert_eq!(cpu.state().upc, 0);
    assert_eq!(
        ram.read_u64(frame).unwrap(),
        u64::from(PageFaultReason::NotPresent.code()) | 0x2300_0100
    );
    assert_eq!(ram.read_u64(frame + 8).unwrap(), 0x1000);
    assert_eq!(ram.read_u64(frame + 16).unwrap(), 0x1000);
    assert_eq!(ram.read_u64(frame + 24).unwrap(), 0);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0);
    assert_eq!(cpu.state().sp, 0);
    assert_eq!(cpu.state().status, Status::empty());
    assert_eq!(cpu.state().status.event_depth(), 0);
    assert!(!cpu.state().hidden_current_dfa);
}

#[test]
fn page_fault_and_double_fault_delivery_failure_enters_shutdown() {
    let mut ram = Ram::new(0x20_000);
    install_four_level_root(&mut ram);
    map_low_page(&mut ram, 0, 0x8000, PTE_X | PTE_U);
    ram.load(0x8000, &[0xc1, 0x18, 0x80]).unwrap();

    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = Status::empty();
    cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
    configure_event_entry(&mut cpu, 0x5000, 0x7000);
    cpu.state_mut().r[0] = 0x1000;

    assert_eq!(cpu.step(&mut ram), StepResult::Halted);
    assert!(cpu.is_halted());
    assert_eq!(cpu.state().pc, 0);
    assert_eq!(cpu.state().status, Status::empty());
}

#[test]
fn resume_flag_suppresses_exactly_one_trace_event() {
    let mut ram = Ram::new(0x2000);
    ram.load(0, &[0x01, 0x01]).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = Status::TF | Status::RF;
    configure_event_entry(&mut cpu, 0x100, 0x1000);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 1);
    assert!(cpu.state().status.contains(Status::TF));
    assert!(!cpu.state().status.contains(Status::RF));

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x100);
    assert_eq!(cpu.state().uinfo, 0);
    assert_eq!(cpu.state().upc, 2);
    assert!(!cpu.state().status.intersects(Status::TF | Status::RF));
}
