use std::env;
use std::path::PathBuf;
use std::process::Command;

fn main() {
    println!("cargo:rerun-if-env-changed=BEDROCK_LLVM_ROOT");
    println!("cargo:rerun-if-env-changed=BEDROCK_LLVM_BIN");
    println!("cargo:rerun-if-env-changed=CXX");
    println!("cargo:rerun-if-env-changed=AR");
    println!("cargo:rerun-if-changed=src/shim.cpp");

    let source_include = bedrock_toolchain::default_lldb_source_include_dir()
        .unwrap_or_else(|error| panic!("failed to resolve LLDB source include directory: {error}"));
    let build_include = bedrock_toolchain::default_lldb_build_include_dir()
        .unwrap_or_else(|error| panic!("failed to resolve LLDB build include directory: {error}"));
    let lib_dir = bedrock_toolchain::default_lib_dir()
        .unwrap_or_else(|error| panic!("failed to resolve LLVM library directory: {error}"));

    if !source_include
        .join("lldb")
        .join("API")
        .join("SBDebugger.h")
        .is_file()
    {
        panic!(
            "missing LLDB source headers under {}",
            source_include.display()
        );
    }
    if !build_include.join("lldb").join("LLDB.h").is_file() {
        panic!(
            "missing LLDB build headers under {}",
            build_include.display()
        );
    }
    if !lib_dir.join("liblldb.dylib").is_file() && !lib_dir.join("liblldb.so").is_file() {
        panic!("missing liblldb under {}", lib_dir.display());
    }

    let out_dir = PathBuf::from(env::var_os("OUT_DIR").expect("OUT_DIR is set by Cargo"));
    let object = out_dir.join("bedrock_lldb_shim.o");
    let archive = out_dir.join("libbedrock_lldb_shim.a");

    run(
        cxx(),
        [
            "-std=c++17".into(),
            "-Wno-deprecated-declarations".into(),
            "-c".into(),
            "src/shim.cpp".into(),
            format!("-I{}", source_include.display()),
            format!("-I{}", build_include.display()),
            "-o".into(),
            object.display().to_string(),
        ],
    );
    run(
        ar(),
        [
            "crus".into(),
            archive.display().to_string(),
            object.display().to_string(),
        ],
    );

    println!("cargo:rustc-link-search=native={}", out_dir.display());
    println!("cargo:rustc-link-lib=static=bedrock_lldb_shim");
    println!("cargo:rustc-link-search=native={}", lib_dir.display());
    println!("cargo:rustc-link-lib=dylib=lldb");

    #[cfg(target_os = "macos")]
    {
        println!("cargo:rustc-link-lib=c++");
        println!("cargo:rustc-link-arg=-Wl,-rpath,{}", lib_dir.display());
    }

    #[cfg(target_os = "linux")]
    {
        println!("cargo:rustc-link-arg=-Wl,-rpath,{}", lib_dir.display());
    }
}

fn cxx() -> String {
    env::var("CXX").unwrap_or_else(|_| "clang++".to_owned())
}

fn ar() -> String {
    env::var("AR").unwrap_or_else(|_| "ar".to_owned())
}

fn run<I>(program: String, args: I)
where
    I: IntoIterator<Item = String>,
{
    let args: Vec<String> = args.into_iter().collect();
    let output = Command::new(&program)
        .args(&args)
        .output()
        .unwrap_or_else(|error| {
            panic!(
                "failed to run {}: {}",
                display_command(&program, &args),
                error
            )
        });

    if !output.status.success() {
        panic!(
            "{} failed with status {}\nstdout:\n{}\nstderr:\n{}",
            display_command(&program, &args),
            output.status,
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
    }
}

fn display_command(program: &str, args: &[String]) -> String {
    let mut text = program.to_owned();
    for arg in args {
        text.push(' ');
        text.push_str(arg);
    }
    text
}
