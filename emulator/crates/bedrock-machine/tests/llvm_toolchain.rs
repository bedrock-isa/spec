use bedrock_core::StepResult;
use bedrock_machine::{ElfLoadOptions, Machine};
use std::path::PathBuf;

const TTY_STATE: usize = 0x0002_2000;
const MARKERS: usize = TTY_STATE + 8;
const SYSCALL_COUNT: usize = TTY_STATE + 0x98;
const PRESSED: u32 = 0x0001_0000;
const PTE_PRESENT: u64 = 1 << 0;
const PTE_WRITE: u64 = 1 << 1;
const PTE_EXEC: u64 = 1 << 2;
const PTE_USER: u64 = 1 << 3;

fn tiny_kernel_elf() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../samples/tiny_kernel/build/tiny_kernel.elf")
}

fn marker(machine: &Machine, offset: usize) -> u8 {
    machine.board().ram().as_slice()[MARKERS + offset]
}

fn leaf_pte(machine: &Machine, virtual_address: u64) -> u64 {
    let ram = machine.board().ram().as_slice();
    let mut table = machine.state().ptcr.root_table_addr() as usize;
    for shift in [39, 30, 21, 12] {
        let index = ((virtual_address >> shift) & 0x1ff) as usize;
        let address = table + index * 8;
        let entry = u64::from_le_bytes(ram[address..address + 8].try_into().unwrap());
        assert_ne!(
            entry & PTE_PRESENT,
            0,
            "missing PTE for {virtual_address:#x}"
        );
        if shift == 12 {
            return entry;
        }
        table = (entry & !0xfff) as usize;
    }
    unreachable!()
}

fn run_until(machine: &mut Machine, limit: u64, mut done: impl FnMut(&Machine) -> bool) -> u64 {
    let mut recent = [0u64; 16];
    for (recent_index, step) in (0..limit).enumerate() {
        if done(machine) {
            return step;
        }
        let pc = machine.state().pc;
        recent[recent_index % recent.len()] = pc;
        match machine.step() {
            StepResult::Running => {}
            result => {
                let sp = machine.state().sp as usize;
                let return_pc = machine
                    .board()
                    .ram()
                    .as_slice()
                    .get(sp..sp + 8)
                    .map(|bytes| u64::from_le_bytes(bytes.try_into().unwrap()));
                let ram = machine.board().ram().as_slice();
                let tty_col = u32::from_le_bytes(ram[TTY_STATE..TTY_STATE + 4].try_into().unwrap());
                let tty_row =
                    u32::from_le_bytes(ram[TTY_STATE + 4..TTY_STATE + 8].try_into().unwrap());
                panic!(
                    "tiny kernel stopped at pc={pc:#x}: {result:?}; recent={recent:?}; registers={:?}; sp={sp:#x}; stack={:?}; return={return_pc:?}; tty={tty_col},{tty_row}",
                    &machine.state().r,
                    ram.get(sp..sp.saturating_add(96)),
                )
            }
        }
    }
    let ram = machine.board().ram().as_slice();
    let tty_col = u32::from_le_bytes(ram[TTY_STATE..TTY_STATE + 4].try_into().unwrap());
    let tty_row = u32::from_le_bytes(ram[TTY_STATE + 4..TTY_STATE + 8].try_into().unwrap());
    let syscall_count =
        u64::from_le_bytes(ram[SYSCALL_COUNT..SYSCALL_COUNT + 8].try_into().unwrap());
    panic!(
        "tiny kernel did not reach the expected state in {limit} steps (pc={:#x}, status={:?}, tty={tty_col},{tty_row}, syscalls={syscall_count}, markers=[58:{:#x},60:{:#x},61:{:#x},62:{:#x},68:{:#x},70:{:#x},75:{:#x},78:{:#x},79:{:#x},5e:{:#x}], keys={})",
        machine.state().pc,
        machine.state().status,
        marker(machine, 0x58),
        marker(machine, 0x60),
        marker(machine, 0x61),
        marker(machine, 0x62),
        marker(machine, 0x68),
        marker(machine, 0x70),
        marker(machine, 0x75),
        marker(machine, 0x78),
        marker(machine, 0x79),
        marker(machine, 0x5e),
        machine.board().keyboard().queued_len(),
    );
}

fn type_command(machine: &mut Machine, command: &str) {
    for byte in command.bytes().chain([b'\n']) {
        machine
            .board_mut()
            .keyboard_mut()
            .push_event(PRESSED | u32::from(byte));
    }
}

#[test]
#[ignore = "requires the freshly built tiny_kernel ELF"]
fn machine_executes_tiny_kernel_sample_with_syscall_and_event_return() {
    let bytes = std::fs::read(tiny_kernel_elf()).expect("build tiny_kernel.elf first");
    let mut machine = Machine::new();
    machine
        .load_elf(&bytes, ElfLoadOptions::default())
        .expect("load tiny kernel ELF");

    run_until(&mut machine, 1_500_000, |machine| {
        !machine.state().status.contains(bedrock_core::Status::PM)
    });
    let shell_root = machine.state().ptcr.root_table_addr();
    assert!(machine.state().ptcr.paging_enabled());
    assert!(machine.state().ascr.asid_enabled());
    assert_eq!(machine.state().ascr.asid(), 1);
    let kernel_text = leaf_pte(&machine, 0x1000);
    assert_eq!(kernel_text & (PTE_WRITE | PTE_EXEC | PTE_USER), PTE_EXEC);
    let shell_text = leaf_pte(&machine, machine.state().pc);
    assert_eq!(
        shell_text & (PTE_WRITE | PTE_EXEC | PTE_USER),
        PTE_EXEC | PTE_USER
    );
    let shell_stack = leaf_pte(&machine, machine.state().sp - 1);
    assert_eq!(
        shell_stack & (PTE_WRITE | PTE_EXEC | PTE_USER),
        PTE_WRITE | PTE_USER
    );

    type_command(&mut machine, "MATH");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 1 && marker(machine, 0x68) != 0
    });

    assert_eq!(marker(&machine, 0x60), 0x51);
    assert_eq!(marker(&machine, 0x62), 0x07);

    type_command(&mut machine, "SORT");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 2 && marker(machine, 0x69) != 0
    });
    assert_eq!(marker(&machine, 0x62), 0x08);

    type_command(&mut machine, "MEM");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 3 && marker(machine, 0x6a) != 0
    });
    assert_eq!(marker(&machine, 0x62), 0x09);

    type_command(&mut machine, "DEMO");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 4 && marker(machine, 0x62) == 0x01
    });

    type_command(&mut machine, "FAULT");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 5 && marker(machine, 0x63) == 0x1d
    });
    assert_eq!(marker(&machine, 0x62), 0x02);

    type_command(&mut machine, "BASIC");
    run_until(&mut machine, 16_000_000, |machine| {
        marker(machine, 0x61) == 6
            && marker(machine, 0x62) == 0x0a
            && marker(machine, 0x70) == 1
            && marker(machine, 0x75) == 1
    });
    assert_eq!(machine.state().ascr.asid(), 2);
    assert_ne!(machine.state().ptcr.root_table_addr(), shell_root);
    let basic_text = leaf_pte(&machine, 0x80000);
    assert_eq!(
        basic_text & (PTE_WRITE | PTE_EXEC | PTE_USER),
        PTE_EXEC | PTE_USER
    );
    type_command(&mut machine, "RUN");
    type_command(&mut machine, "EXIT");
    run_until(&mut machine, 16_000_000, |machine| {
        marker(machine, 0x78) != 0
    });
    assert_eq!(machine.state().ascr.asid(), 1);
    assert_eq!(machine.state().ptcr.root_table_addr(), shell_root);

    type_command(&mut machine, "FAR");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 7
            && marker(machine, 0x62) == 0x0b
            && marker(machine, 0x6f) == 0xaa
            && marker(machine, 0x78) == 0xaa
    });

    type_command(&mut machine, "PFAULT");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 8
            && marker(machine, 0x62) == 0x0c
            && marker(machine, 0x79) == 1
            && machine.state().ascr.asid() == 1
    });
    assert_eq!(machine.state().ascr.asid(), 1);
    assert_eq!(machine.state().ptcr.root_table_addr(), shell_root);

    type_command(&mut machine, "SFAULT");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 9
            && marker(machine, 0x62) == 0x0d
            && marker(machine, 0x79) == 4
            && machine.state().ascr.asid() == 1
    });
    assert_eq!(machine.state().ascr.asid(), 1);
    assert_eq!(machine.state().ptcr.root_table_addr(), shell_root);

    type_command(&mut machine, "HALT");
    run_until(&mut machine, 8_000_000, |machine| {
        marker(machine, 0x61) == 10 && marker(machine, 0x50) == 0xff
    });
    assert_eq!(marker(&machine, 0x62), 0x03);

    assert_eq!(marker(&machine, 0x5e), 0);
    assert!(
        machine
            .board()
            .framebuffer()
            .vram()
            .iter()
            .any(|pixel| *pixel != 0)
    );
    assert!(!machine.board().keyboard().has_overflowed());
}
