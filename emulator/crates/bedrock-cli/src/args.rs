use clap::Parser;
use std::ffi::OsString;
use std::path::PathBuf;

#[derive(Debug, Clone, PartialEq, Eq, Parser)]
#[command(name = "bedrock-cli")]
#[command(about = "Headless Bedrock emulator runner")]
pub struct CliArgs {
    #[arg(long)]
    #[arg(value_name = "PATH")]
    #[arg(conflicts_with = "pc")]
    pub elf: Option<PathBuf>,

    #[arg(long)]
    #[arg(default_value = "0")]
    #[arg(value_parser = parse_u64)]
    #[arg(value_name = "ADDR")]
    pub pc: u64,

    #[arg(long)]
    #[arg(default_value = "0")]
    #[arg(value_parser = parse_u64)]
    #[arg(value_name = "ADDR")]
    #[arg(requires = "elf")]
    pub load_base: u64,

    #[arg(long)]
    #[arg(default_value = "1")]
    #[arg(value_parser = parse_u64)]
    #[arg(value_name = "COUNT")]
    pub steps: u64,

    #[arg(long)]
    #[arg(value_name = "ADDR")]
    pub gdb_remote: Option<String>,
}

impl CliArgs {
    pub fn parse_args() -> Self {
        Self::parse()
    }

    pub fn try_parse_args_from<I, T>(itr: I) -> Result<Self, clap::Error>
    where
        I: IntoIterator<Item = T>,
        T: Into<OsString> + Clone,
    {
        Self::try_parse_from(itr)
    }

    pub fn into_run_config(self) -> RunConfig {
        let image = match self.elf {
            Some(path) => ImageSource::Elf {
                path,
                load_base: self.load_base,
            },
            None => ImageSource::Reset { pc: self.pc },
        };

        RunConfig {
            image,
            steps: self.steps,
            gdb_remote: self.gdb_remote,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RunConfig {
    pub image: ImageSource,
    pub steps: u64,
    pub gdb_remote: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ImageSource {
    Reset { pc: u64 },
    Elf { path: PathBuf, load_base: u64 },
}

fn parse_u64(raw: &str) -> Result<u64, String> {
    let compact: String = raw.chars().filter(|ch| *ch != '_').collect();
    let (digits, radix) = compact
        .strip_prefix("0x")
        .or_else(|| compact.strip_prefix("0X"))
        .map(|digits| (digits, 16))
        .unwrap_or((&compact, 10));

    if digits.is_empty() {
        return Err("expected digits".to_owned());
    }

    u64::from_str_radix(digits, radix).map_err(|err| err.to_string())
}

#[cfg(test)]
mod tests {
    use super::{CliArgs, ImageSource, RunConfig};
    use std::path::PathBuf;

    #[test]
    fn defaults_to_reset_at_zero_for_one_step() {
        let args = CliArgs::try_parse_args_from(["bedrock-cli"]).unwrap();

        assert_eq!(
            args.into_run_config(),
            RunConfig {
                image: ImageSource::Reset { pc: 0 },
                steps: 1,
                gdb_remote: None,
            }
        );
    }

    #[test]
    fn parses_hex_and_underscored_numbers() {
        let args =
            CliArgs::try_parse_args_from(["bedrock-cli", "--pc", "0x1_000", "--steps", "10_000"])
                .unwrap();

        assert_eq!(
            args.into_run_config(),
            RunConfig {
                image: ImageSource::Reset { pc: 0x1000 },
                steps: 10_000,
                gdb_remote: None,
            }
        );
    }

    #[test]
    fn parses_elf_load_request() {
        let args = CliArgs::try_parse_args_from([
            "bedrock-cli",
            "--elf",
            "program.elf",
            "--load-base",
            "0x4000",
            "--steps",
            "0",
        ])
        .unwrap();

        assert_eq!(
            args.into_run_config(),
            RunConfig {
                image: ImageSource::Elf {
                    path: PathBuf::from("program.elf"),
                    load_base: 0x4000,
                },
                steps: 0,
                gdb_remote: None,
            }
        );
    }

    #[test]
    fn parses_gdb_remote_listener() {
        let args = CliArgs::try_parse_args_from(["bedrock-cli", "--gdb-remote", "127.0.0.1:9001"])
            .unwrap();

        assert_eq!(
            args.into_run_config(),
            RunConfig {
                image: ImageSource::Reset { pc: 0 },
                steps: 1,
                gdb_remote: Some("127.0.0.1:9001".to_owned()),
            }
        );
    }

    #[test]
    fn rejects_load_base_without_elf() {
        let err =
            CliArgs::try_parse_args_from(["bedrock-cli", "--load-base", "0x4000"]).unwrap_err();

        assert_eq!(err.kind(), clap::error::ErrorKind::MissingRequiredArgument);
    }

    #[test]
    fn rejects_pc_override_when_elf_is_loaded() {
        let err =
            CliArgs::try_parse_args_from(["bedrock-cli", "--elf", "program.elf", "--pc", "4"])
                .unwrap_err();

        assert_eq!(err.kind(), clap::error::ErrorKind::ArgumentConflict);
    }
}
