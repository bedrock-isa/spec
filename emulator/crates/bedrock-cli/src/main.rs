use bedrock_cli::{CliArgs, ImageSource};
use bedrock_debug::Debugger;
use bedrock_machine::{ElfLoadOptions, Machine};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = CliArgs::parse_args().into_run_config();
    let mut machine = Machine::new();
    let mut debugger = Debugger::default();

    match config.image {
        ImageSource::Elf { path, load_base } => {
            let bytes = std::fs::read(&path)?;
            let result = machine.load_elf(&bytes, ElfLoadOptions { load_base })?;
            println!(
                "loaded {path:?}: entry=0x{:016x}, segments={}",
                result.entry,
                result.segments.len()
            );
        }
        ImageSource::Reset { pc } => {
            machine.processor_reset(pc);
        }
    }

    if let Some(addr) = config.gdb_remote {
        println!("listening for LLDB/GDB remote debugger on {addr}");
        bedrock_debug_remote::run_tcp(addr.as_str(), &mut machine, &mut debugger)?;
        return Ok(());
    }

    for _ in 0..config.steps {
        let result = debugger.step(&mut machine);
        println!("{result:?}");
        if !matches!(result, bedrock_debug::StepResult::Running) {
            break;
        }
    }

    Ok(())
}
