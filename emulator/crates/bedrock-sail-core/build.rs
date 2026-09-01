use std::env;
use std::ffi::OsString;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

const GENERATOR_INPUTS: &[&str] = &[
    "artifacts/emulator-core",
    "artifacts/sail-model",
    "artifacts/schema.yaml",
    "engine",
    "isa",
];
const MAX_GENERATED_C_FRAME_BYTES: u64 = 48 * 1024;
const MAX_GENERATED_C_INITIALIZER_FRAME_BYTES: u64 = 32 * 1024;
const C_BUILD_CONFIGURATION: &str = "c11-o3-no-semantic-interposition-v1";

fn canonicalize(path: &Path, description: &str) -> PathBuf {
    path.canonicalize().unwrap_or_else(|error| {
        panic!(
            "failed to resolve {description} {}: {error}",
            path.display()
        )
    })
}

fn emit_rerun_inputs(path: &Path) {
    if path.is_file() {
        println!("cargo:rerun-if-changed={}", path.display());
        return;
    }
    let mut entries = fs::read_dir(path)
        .unwrap_or_else(|error| panic!("failed to inspect {}: {error}", path.display()))
        .map(|entry| {
            entry
                .expect("failed to inspect generator input entry")
                .path()
        })
        .collect::<Vec<_>>();
    entries.sort();
    for entry in entries {
        let name = entry.file_name().and_then(|name| name.to_str());
        if name == Some("__pycache__") || name.is_some_and(|name| name.starts_with('.')) {
            continue;
        }
        emit_rerun_inputs(&entry);
    }
}

fn command_output(mut command: Command, description: &str) -> String {
    let output = command
        .output()
        .unwrap_or_else(|error| panic!("failed to run {description}: {error}"));
    if !output.status.success() {
        panic!(
            "{description} failed with {}\nstdout:\n{}\nstderr:\n{}",
            output.status,
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr),
        );
    }
    String::from_utf8(output.stdout)
        .unwrap_or_else(|error| panic!("{description} produced non-UTF-8 output: {error}"))
}

fn stack_usage_files(root: &Path, files: &mut Vec<PathBuf>) {
    for entry in fs::read_dir(root)
        .unwrap_or_else(|error| panic!("failed to inspect {}: {error}", root.display()))
    {
        let path = entry
            .expect("failed to inspect compiler output entry")
            .path();
        if path.is_dir() {
            stack_usage_files(&path, files);
        } else if path.extension().is_some_and(|extension| extension == "su") {
            files.push(path);
        }
    }
}

fn validate_stack_usage(out_dir: &Path) {
    let mut files = Vec::new();
    stack_usage_files(out_dir, &mut files);
    if files.is_empty() {
        panic!(
            "C compiler did not emit -fstack-usage data beneath {}",
            out_dir.display()
        );
    }

    let mut largest_runtime = (0, String::new());
    let mut largest_initializer = (0, String::new());
    for path in files {
        let content = fs::read_to_string(&path)
            .unwrap_or_else(|error| panic!("failed to read {}: {error}", path.display()));
        for line in content.lines() {
            let mut fields = line.split('\t');
            let function = fields.next().unwrap_or_default();
            let Some(bytes) = fields.next().and_then(|value| value.parse::<u64>().ok()) else {
                continue;
            };
            let largest = if function
                .rsplit(':')
                .next()
                .is_some_and(|name| name.starts_with("create_letbind_"))
            {
                &mut largest_initializer
            } else {
                &mut largest_runtime
            };
            if bytes > largest.0 {
                *largest = (bytes, function.to_owned());
            }
        }
    }
    if largest_runtime.0 > MAX_GENERATED_C_FRAME_BYTES {
        panic!(
            "generated C stack frame is {} bytes in {}, exceeding the {}-byte limit",
            largest_runtime.0, largest_runtime.1, MAX_GENERATED_C_FRAME_BYTES
        );
    }
    if largest_initializer.0 > MAX_GENERATED_C_INITIALIZER_FRAME_BYTES {
        panic!(
            "generated C initializer stack frame is {} bytes in {}, exceeding the {}-byte limit",
            largest_initializer.0, largest_initializer.1, MAX_GENERATED_C_INITIALIZER_FRAME_BYTES
        );
    }
}

fn generate_operation_constants(header: &Path, out_dir: &Path) {
    let source = fs::read_to_string(header)
        .unwrap_or_else(|error| panic!("failed to read {}: {error}", header.display()));
    let marker = "enum zSemantic_operation {";
    let start = source
        .find(marker)
        .unwrap_or_else(|| panic!("{} has no Semantic_operation enum", header.display()))
        + marker.len();
    let end = source[start..]
        .find("};")
        .map(|offset| start + offset)
        .unwrap_or_else(|| {
            panic!(
                "{} has an unterminated Semantic_operation enum",
                header.display()
            )
        });
    let mut rust = String::from("// Generated from Sail's Semantic_operation enum.\n");
    for (ordinal, raw) in source[start..end].split(',').enumerate() {
        let name = raw
            .trim()
            .strip_prefix("zOp_")
            .unwrap_or_else(|| panic!("unexpected Semantic_operation enumerator {raw:?}"));
        let constant = name
            .chars()
            .map(|character| {
                if character.is_ascii_alphanumeric() {
                    character.to_ascii_uppercase()
                } else {
                    '_'
                }
            })
            .collect::<String>();
        rust.push_str(&format!("pub const OP_{constant}: i32 = {ordinal};\n"));
    }
    fs::write(out_dir.join("semantic_operations.rs"), rust)
        .expect("failed to write generated Semantic_operation constants");
}

fn main() {
    println!("cargo:rerun-if-env-changed=PYTHON");
    println!("cargo:rerun-if-env-changed=SAIL");

    let crate_dir = PathBuf::from(
        env::var_os("CARGO_MANIFEST_DIR").expect("Cargo did not set CARGO_MANIFEST_DIR"),
    );
    let repository_root = canonicalize(&crate_dir.join("../../.."), "repository root");
    for input in GENERATOR_INPUTS {
        emit_rerun_inputs(&repository_root.join(input));
    }

    let out_dir = PathBuf::from(env::var_os("OUT_DIR").expect("Cargo did not set OUT_DIR"));
    let generated_root = out_dir.join("emulator-core");
    let python = env::var_os("PYTHON")
        .filter(|value| !value.is_empty())
        .unwrap_or_else(|| OsString::from("python3"));
    let sail = env::var_os("SAIL")
        .filter(|value| !value.is_empty())
        .unwrap_or_else(|| OsString::from("sail"));

    let mut generate = Command::new(&python);
    generate
        .current_dir(&repository_root)
        .args([
            "-m",
            "engine",
            "artifacts",
            "generate",
            "emulator-core",
            "--output",
        ])
        .arg(&generated_root)
        .env("PYTHONDONTWRITEBYTECODE", "1");
    command_output(generate, "emulator-core artifact generator");

    let core_dir = generated_root.join("emulator/core");
    let core_c = core_dir.join("bedrock_core.c");
    if !core_c.is_file() {
        panic!(
            "emulator-core generator did not create {}",
            core_c.display()
        );
    }
    generate_operation_constants(&core_dir.join("bedrock_core.h"), &out_dir);

    let mut sail_dir_command = Command::new(&sail);
    sail_dir_command.arg("-dir");
    let sail_lib = PathBuf::from(command_output(sail_dir_command, "sail -dir").trim()).join("lib");
    let gmp = pkg_config::Config::new()
        .probe("gmp")
        .unwrap_or_else(|error| panic!("failed to locate GMP with pkg-config: {error}"));

    let generation_stamp = fs::read_to_string(core_dir.join(".generation-stamp"))
        .expect("emulator-core generator did not create its generation stamp");
    let compiled_fingerprint = format!("{generation_stamp}{C_BUILD_CONFIGURATION}\n");
    let compiled_stamp = out_dir.join("bedrock_sail_core.stamp");
    let compiled_library = out_dir.join("libbedrock_sail_core.a");
    if compiled_library.is_file()
        && fs::read_to_string(&compiled_stamp).is_ok_and(|stamp| stamp == compiled_fingerprint)
    {
        println!("cargo:rustc-link-search=native={}", out_dir.display());
        println!("cargo:rustc-link-lib=static=bedrock_sail_core");
        validate_stack_usage(&out_dir);
        return;
    }

    let mut build = cc::Build::new();
    build
        .std("c11")
        // Sail's generated temporaries cause multi-megabyte frames at -O0.
        // Keep the C core optimized independently of Cargo's Rust profile.
        .opt_level(3)
        .debug(false)
        .warnings(false)
        .flag_if_supported("-fno-semantic-interposition")
        .flag_if_supported("-fstack-usage")
        .include(&core_dir)
        .include(&sail_lib)
        .file(core_c);
    for source in [
        "sail.c",
        "rts.c",
        "elf.c",
        "sail_config.c",
        "sail_failure.c",
        "cJSON.c",
    ] {
        build.file(sail_lib.join(source));
    }
    for include in gmp.include_paths {
        build.include(include);
    }
    build.compile("bedrock_sail_core");
    fs::write(&compiled_stamp, compiled_fingerprint)
        .unwrap_or_else(|error| panic!("failed to write {}: {error}", compiled_stamp.display()));
    validate_stack_usage(&out_dir);
}
