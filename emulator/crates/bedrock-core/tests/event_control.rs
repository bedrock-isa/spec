use bedrock_bus::{Bus, Ram};
use bedrock_core::{
    AddressSpaceControl, Cpu, EventControl, ExceptionFrameType, PageFaultReason, PageTableControl,
    Status, StepResult,
};

const PTE_P: u64 = 1 << 0;
const PTE_W: u64 = 1 << 1;
const PTE_X: u64 = 1 << 2;
const PTE_U: u64 = 1 << 3;
const PTE_T: u64 = 1 << 11;

fn configure_event_entry(cpu: &mut Cpu, epc: u64, fsp: u64) {
    cpu.state_mut().ecr = EventControl::from_raw(1);
    cpu.state_mut().epc = epc;
    cpu.state_mut().fsp = fsp;
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

#[test]
fn illegal_instruction_delivers_typed_error_frame_with_zero_padding() {
    let mut ram = Ram::new(0x2000);
    ram.write_u8(0, 0x00).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    configure_event_entry(&mut cpu, 0x100, 0x1000);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x100);
    assert_eq!(cpu.state().sp, 0xfb0);
    assert_eq!(
        ram.read_u64(0xfb0).unwrap() & 0xfff,
        (u64::from(ExceptionFrameType::Error as u8) << 8) | 10
    );
    assert_eq!(ram.read_u64(0xfb8).unwrap(), 0x03);
    assert_eq!(ram.read_u64(0xfc8).unwrap(), 0);
    assert_eq!(ram.read_u64(0xff0).unwrap(), 4);
    assert_eq!(ram.read_u64(0xff8).unwrap(), 0);
}

#[test]
fn debug_trace_commits_the_unit_then_saves_the_next_boundary() {
    let mut ram = Ram::new(0x2000);
    ram.write_u8(0, 0x01).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status.insert(Status::TF);
    configure_event_entry(&mut cpu, 0x100, 0x1000);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x100);
    assert_eq!(cpu.state().sp, 0xfc0);
    assert_eq!(ram.read_u64(0xfc0).unwrap() & 0xfff, 8);
    assert_eq!(ram.read_u64(0xfc8).unwrap(), 0);
    assert_eq!(ram.read_u64(0xfd8).unwrap(), 1);
    assert_ne!((ram.read_u64(0xfc0).unwrap() >> 48) & 4, 0);
    assert!(!cpu.state().status.contains(Status::TF));
}

#[test]
fn malformed_eret_frame_delivers_invalid_control_without_consuming_it() {
    let mut ram = Ram::new(0x3000);
    ram.write_u8(0, 0x04).unwrap();
    let mut cpu = Cpu::new();
    cpu.reset(0);
    cpu.state_mut().status = Status::PM | Status::EA;
    cpu.state_mut().hidden_current_edepth = 1;
    cpu.state_mut().hidden_current_esl = 2;
    cpu.state_mut().sp = 0x1000;
    configure_event_entry(&mut cpu, 0x200, 0x1800);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0x200);
    assert_eq!(cpu.state().sp, 0xfb0);
    assert_eq!(cpu.state().hidden_current_edepth, 2);
    assert_eq!(ram.read_u64(0xfb8).unwrap(), 0x0d);
    assert_eq!(ram.read_u64(0xfc8).unwrap(), 0);
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
    assert_eq!(cpu.state().sp, 0x6fa0);
    assert!(cpu.state().status.contains(Status::PM | Status::EA));
    assert_eq!(cpu.state().r[1], 0xfeed_face);

    let frame = 0xefa0;
    assert_eq!(
        ram.read_u64(frame).unwrap() & 0xfff,
        (u64::from(ExceptionFrameType::PageFault as u8) << 8) | 12
    );
    assert_eq!(ram.read_u64(frame + 8).unwrap(), 9);
    assert_eq!(ram.read_u64(frame + 24).unwrap(), 0);
    assert_eq!(
        ram.read_u64(frame + 64).unwrap(),
        u64::from(PageFaultReason::NotPresent.code()) | 0x2300_0100
    );
    assert_eq!(ram.read_u64(frame + 72).unwrap(), 0x1000);
    assert_eq!(ram.read_u64(frame + 80).unwrap(), 0x1000);
    assert_eq!(ram.read_u64(frame + 88).unwrap(), 0);

    assert_eq!(cpu.step(&mut ram), StepResult::Running);
    assert_eq!(cpu.state().pc, 0);
    assert_eq!(cpu.state().sp, 0);
    assert_eq!(cpu.state().status, Status::empty());
    assert_eq!(cpu.state().hidden_current_edepth, 0);
    assert_eq!(cpu.state().hidden_current_esl, 0);
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
    assert_eq!(ram.read_u64(0xfc8).unwrap(), 0);
    assert_eq!(ram.read_u64(0xfd8).unwrap(), 2);
    assert!(!cpu.state().status.intersects(Status::TF | Status::RF));
}
