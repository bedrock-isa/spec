use bedrock_machine::{ElfLoadOptions, Machine, StepResult};
use bedrock_toolchain::{LinkOptions, LlvmToolchain};
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

struct TestDirectory(PathBuf);

impl TestDirectory {
    fn create() -> std::io::Result<Self> {
        let nonce = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("system clock must follow the Unix epoch")
            .as_nanos();
        let path =
            std::env::temp_dir().join(format!("bedrock-elf-smoke-{}-{nonce}", std::process::id()));
        std::fs::create_dir(&path)?;
        Ok(Self(path))
    }

    fn path(&self) -> &Path {
        &self.0
    }
}

impl Drop for TestDirectory {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

#[test]
fn llvm_elf_executes_in_sail_machine() -> Result<(), Box<dyn std::error::Error>> {
    let toolchain = LlvmToolchain::discover()?;
    let directory = TestDirectory::create()?;
    let source = Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/elf_smoke.s");
    let object = directory.path().join("elf_smoke.o");
    let executable = directory.path().join("elf_smoke.elf");

    toolchain.assemble_object(&source, &object)?;
    toolchain.link_executable(&object, &executable, LinkOptions::default())?;

    let bytes = std::fs::read(executable)?;
    let mut machine = Machine::new();
    let loaded = machine.load_elf(&bytes, ElfLoadOptions::default())?;

    assert_eq!(loaded.entry, 0x1000);
    assert_eq!(machine.state().pc, 0x1000);
    assert_eq!(machine.step(), StepResult::Running);
    assert_eq!(machine.state().r[0], 42);
    assert_eq!(machine.state().pc, 0x1004);
    assert_eq!(machine.step(), StepResult::Halted);
    assert_eq!(machine.state().r[0], 42);
    assert_eq!(machine.state().pc, 0x1006);
    Ok(())
}
