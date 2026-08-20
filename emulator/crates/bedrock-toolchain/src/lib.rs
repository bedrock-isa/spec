use std::env;
use std::ffi::{OsStr, OsString};
use std::path::{Path, PathBuf};
use std::process::{Command, ExitStatus, Output};
use thiserror::Error;

pub const BEDROCK_TRIPLE: &str = "bedrock-unknown-unknown";
pub const BEDROCK_LLD_EMULATION: &str = "elf64bedrock";
pub const BEDROCK_LLVM_BIN_ENV: &str = "BEDROCK_LLVM_BIN";
pub const BEDROCK_LLVM_ROOT_ENV: &str = "BEDROCK_LLVM_ROOT";

const LLVM_MC: &str = "llvm-mc";
const CLANG: &str = "clang";
const LD_LLD: &str = "ld.lld";
const LLVM_OBJDUMP: &str = "llvm-objdump";
const REQUIRED_TOOLS: &[&str] = &[LLVM_MC, CLANG, LD_LLD, LLVM_OBJDUMP];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LlvmToolchain {
    bin_dir: PathBuf,
}

impl LlvmToolchain {
    pub fn discover() -> Result<Self, ToolchainError> {
        Self::from_bin_dir(default_bin_dir()?)
    }

    pub fn from_bin_dir(bin_dir: impl Into<PathBuf>) -> Result<Self, ToolchainError> {
        let toolchain = Self {
            bin_dir: bin_dir.into(),
        };

        for tool in REQUIRED_TOOLS {
            toolchain.require_tool(tool)?;
        }

        Ok(toolchain)
    }

    pub fn bin_dir(&self) -> &Path {
        &self.bin_dir
    }

    pub fn assemble_object(&self, source: &Path, object: &Path) -> Result<(), ToolchainError> {
        self.run(
            LLVM_MC,
            [
                OsString::from(format!("-triple={BEDROCK_TRIPLE}")),
                OsString::from("-filetype=obj"),
                source.as_os_str().to_owned(),
                OsString::from("-o"),
                object.as_os_str().to_owned(),
            ],
        )?;
        Ok(())
    }

    pub fn compile_c_object(&self, source: &Path, object: &Path) -> Result<(), ToolchainError> {
        self.compile_c_object_with_optimization(source, object, "-O2")
    }

    pub fn compile_c_object_with_optimization(
        &self,
        source: &Path,
        object: &Path,
        optimization: &str,
    ) -> Result<(), ToolchainError> {
        self.run(
            CLANG,
            [
                OsString::from("-target"),
                OsString::from(BEDROCK_TRIPLE),
                OsString::from("-ffreestanding"),
                OsString::from("-nostdlib"),
                OsString::from(optimization),
                OsString::from("-c"),
                source.as_os_str().to_owned(),
                OsString::from("-o"),
                object.as_os_str().to_owned(),
            ],
        )?;
        Ok(())
    }

    pub fn link_executable(
        &self,
        object: &Path,
        elf: &Path,
        options: LinkOptions,
    ) -> Result<(), ToolchainError> {
        self.link_executable_objects([object], elf, options)
    }

    pub fn link_executable_objects_with_script<I, P>(
        &self,
        objects: I,
        elf: &Path,
        linker_script: &Path,
    ) -> Result<(), ToolchainError>
    where
        I: IntoIterator<Item = P>,
        P: AsRef<Path>,
    {
        let mut args = vec![
            OsString::from("-m"),
            OsString::from(BEDROCK_LLD_EMULATION),
            OsString::from("-T"),
            linker_script.as_os_str().to_owned(),
        ];
        for object in objects {
            args.push(object.as_ref().as_os_str().to_owned());
        }
        args.extend([OsString::from("-o"), elf.as_os_str().to_owned()]);

        self.run(LD_LLD, args)?;
        Ok(())
    }

    pub fn link_executable_objects<I, P>(
        &self,
        objects: I,
        elf: &Path,
        options: LinkOptions,
    ) -> Result<(), ToolchainError>
    where
        I: IntoIterator<Item = P>,
        P: AsRef<Path>,
    {
        let mut args = vec![OsString::from("-m"), OsString::from(BEDROCK_LLD_EMULATION)];
        for object in objects {
            args.push(object.as_ref().as_os_str().to_owned());
        }
        args.extend([
            OsString::from(format!("--image-base={:#x}", options.image_base)),
            OsString::from(format!("-Ttext={:#x}", options.text_addr)),
            OsString::from("-o"),
            elf.as_os_str().to_owned(),
        ]);

        self.run(LD_LLD, args)?;
        Ok(())
    }

    pub fn disassemble(&self, image: &Path) -> Result<String, ToolchainError> {
        let output = self.run(
            LLVM_OBJDUMP,
            [
                OsString::from("-d"),
                OsString::from("--no-show-raw-insn"),
                image.as_os_str().to_owned(),
            ],
        )?;

        String::from_utf8(output.stdout).map_err(|source| ToolchainError::Utf8 {
            tool: LLVM_OBJDUMP,
            source,
        })
    }

    fn require_tool(&self, tool: &'static str) -> Result<(), ToolchainError> {
        if self.tool_path(tool).is_file() {
            Ok(())
        } else {
            Err(ToolchainError::MissingTool {
                tool,
                bin_dir: self.bin_dir.clone(),
            })
        }
    }

    fn run<I, S>(&self, tool: &'static str, args: I) -> Result<Output, ToolchainError>
    where
        I: IntoIterator<Item = S>,
        S: AsRef<OsStr>,
    {
        let output = Command::new(self.tool_path(tool))
            .args(args)
            .output()
            .map_err(|source| ToolchainError::Spawn { tool, source })?;

        if output.status.success() {
            Ok(output)
        } else {
            Err(ToolchainError::Failed {
                tool,
                status: output.status,
                stdout: String::from_utf8_lossy(&output.stdout).into_owned(),
                stderr: String::from_utf8_lossy(&output.stderr).into_owned(),
            })
        }
    }

    fn tool_path(&self, tool: &str) -> PathBuf {
        self.bin_dir.join(tool_name(tool))
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LinkOptions {
    pub image_base: u64,
    pub text_addr: u64,
}

impl Default for LinkOptions {
    fn default() -> Self {
        Self {
            image_base: 0,
            text_addr: 0x1000,
        }
    }
}

#[derive(Debug, Error)]
pub enum ToolchainError {
    #[error(
        "neither BEDROCK_LLVM_BIN nor BEDROCK_LLVM_ROOT is set; set BEDROCK_LLVM_BIN to the LLVM tool binary directory or BEDROCK_LLVM_ROOT to the LLVM source root"
    )]
    MissingLlvmConfiguration,
    #[error(
        "BEDROCK_LLVM_ROOT is not set; set it to the LLVM source root for LLVM headers and libraries"
    )]
    MissingLlvmRoot,
    #[error("missing LLVM Bedrock tool `{tool}` in {bin_dir:?}")]
    MissingTool {
        tool: &'static str,
        bin_dir: PathBuf,
    },
    #[error("failed to run `{tool}`: {source}")]
    Spawn {
        tool: &'static str,
        #[source]
        source: std::io::Error,
    },
    #[error("{tool} failed with status {status}\nstdout:\n{stdout}\nstderr:\n{stderr}")]
    Failed {
        tool: &'static str,
        status: ExitStatus,
        stdout: String,
        stderr: String,
    },
    #[error("{tool} output is not UTF-8: {source}")]
    Utf8 {
        tool: &'static str,
        #[source]
        source: std::string::FromUtf8Error,
    },
}

pub fn default_bin_dir() -> Result<PathBuf, ToolchainError> {
    llvm_bin_dir_from_config(
        env::var_os(BEDROCK_LLVM_BIN_ENV),
        env::var_os(BEDROCK_LLVM_ROOT_ENV),
    )
}

fn llvm_bin_dir_from_config(
    bin_dir: Option<OsString>,
    llvm_root: Option<OsString>,
) -> Result<PathBuf, ToolchainError> {
    if let Some(bin_dir) = bin_dir {
        return Ok(PathBuf::from(bin_dir));
    }

    if let Some(llvm_root) = llvm_root {
        return Ok(PathBuf::from(llvm_root).join("build").join("bin"));
    }

    Err(ToolchainError::MissingLlvmConfiguration)
}

pub fn default_llvm_root() -> Result<PathBuf, ToolchainError> {
    env::var_os(BEDROCK_LLVM_ROOT_ENV)
        .map(PathBuf::from)
        .ok_or(ToolchainError::MissingLlvmRoot)
}

pub fn default_build_dir() -> Result<PathBuf, ToolchainError> {
    Ok(default_llvm_root()?.join("build"))
}

pub fn default_lib_dir() -> Result<PathBuf, ToolchainError> {
    Ok(default_build_dir()?.join("lib"))
}

pub fn default_lldb_source_include_dir() -> Result<PathBuf, ToolchainError> {
    Ok(default_llvm_root()?.join("lldb").join("include"))
}

pub fn default_lldb_build_include_dir() -> Result<PathBuf, ToolchainError> {
    Ok(default_build_dir()?.join("include"))
}

fn tool_name(name: &str) -> String {
    #[cfg(windows)]
    {
        format!("{name}.exe")
    }

    #[cfg(not(windows))]
    {
        name.to_owned()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bin_configuration_takes_precedence_over_root() {
        let selected = llvm_bin_dir_from_config(
            Some(OsString::from("/configured/bin")),
            Some(OsString::from("/configured/root")),
        )
        .expect("explicit bin configuration should resolve");

        assert_eq!(selected, PathBuf::from("/configured/bin"));
    }

    #[test]
    fn root_configuration_derives_build_bin() {
        let selected = llvm_bin_dir_from_config(None, Some(OsString::from("/configured/root")))
            .expect("root configuration should resolve");

        assert_eq!(selected, PathBuf::from("/configured/root/build/bin"));
    }

    #[test]
    fn missing_configuration_is_an_error() {
        assert!(matches!(
            llvm_bin_dir_from_config(None, None),
            Err(ToolchainError::MissingLlvmConfiguration)
        ));
    }
}
