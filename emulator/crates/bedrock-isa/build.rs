use std::env;
use std::ffi::OsString;
use std::path::{Path, PathBuf};
use std::process::Command;

const GENERATOR_INPUTS: &[&str] = &[
    "emulator/tools/gen_isa.py",
    "isa/defs",
    "isa/tools/encoding_store.py",
    "isa/tools/validate_alloc.py",
    "isa/tools/defs_loader.py",
    "isa/tools/encoding_fields.py",
    "isa/tools/defs_schema.py",
    "isa/tools/encoding_architecture.py",
];

fn canonicalize(path: &Path, description: &str) -> PathBuf {
    path.canonicalize().unwrap_or_else(|error| {
        panic!(
            "failed to resolve {description} {}: {error}",
            path.display()
        )
    })
}

fn main() {
    println!("cargo:rerun-if-env-changed=PYTHON");

    let crate_dir = PathBuf::from(
        env::var_os("CARGO_MANIFEST_DIR").expect("Cargo did not set CARGO_MANIFEST_DIR"),
    );
    let repository_root = canonicalize(&crate_dir.join("../../.."), "repository root");
    for input in GENERATOR_INPUTS {
        println!(
            "cargo:rerun-if-changed={}",
            repository_root.join(input).display()
        );
    }

    let out_dir = PathBuf::from(env::var_os("OUT_DIR").expect("Cargo did not set OUT_DIR"));
    let generated = out_dir.join("generated.rs");
    let generator = repository_root.join("emulator/tools/gen_isa.py");
    let python = env::var_os("PYTHON")
        .filter(|value| !value.is_empty())
        .unwrap_or_else(|| OsString::from("python3"));

    let output = Command::new(&python)
        .arg(&generator)
        .arg("--isa-design")
        .arg(&repository_root)
        .arg("--output")
        .arg(&generated)
        .env("PYTHONDONTWRITEBYTECODE", "1")
        .output()
        .unwrap_or_else(|error| {
            panic!(
                "failed to run ISA generator with {}: {error}",
                Path::new(&python).display()
            )
        });

    if !output.status.success() {
        panic!(
            "ISA generator failed with {}\nstdout:\n{}\nstderr:\n{}",
            output.status,
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr),
        );
    }
    if !generated.is_file() {
        panic!(
            "ISA generator succeeded without creating {}",
            generated.display()
        );
    }
}
