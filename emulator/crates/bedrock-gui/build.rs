fn main() {
    println!("cargo:rerun-if-env-changed=BEDROCK_LLVM_ROOT");
    let lib_dir = bedrock_toolchain::default_lib_dir()
        .unwrap_or_else(|error| panic!("failed to resolve LLVM library directory: {error}"));

    #[cfg(any(target_os = "macos", target_os = "linux"))]
    {
        println!("cargo:rustc-link-arg=-Wl,-rpath,{}", lib_dir.display());
    }
}
