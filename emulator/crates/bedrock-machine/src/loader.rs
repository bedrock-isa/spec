use crate::board::Board;
use bedrock_bus::{Bus, BusError, BusResult};
use thiserror::Error;

pub fn load_binary(board: &mut Board, base_addr: u64, bytes: &[u8]) -> BusResult<()> {
    board.load_ram(base_addr, bytes)
}

pub const EM_BEDROCK: u16 = 0xffb0;

const EI_CLASS: usize = 4;
const EI_DATA: usize = 5;
const EI_VERSION: usize = 6;
const EI_OSABI: usize = 7;
const EI_ABIVERSION: usize = 8;

const ELFCLASS64: u8 = 2;
const ELFDATA2LSB: u8 = 1;
const EV_CURRENT: u8 = 1;
const ELFOSABI_NONE: u8 = 0;

const ET_EXEC: u16 = 2;
const ET_DYN: u16 = 3;

const PT_NULL: u32 = 0;
const PT_LOAD: u32 = 1;
const PT_DYNAMIC: u32 = 2;
const PT_INTERP: u32 = 3;
const PT_NOTE: u32 = 4;
const PT_PHDR: u32 = 6;
const PT_TLS: u32 = 7;
const PT_GNU_STACK: u32 = 0x6474_e551;

const PF_X: u32 = 1;
const PF_W: u32 = 2;
const PF_R: u32 = 4;

const ELF_HEADER_SIZE: u16 = 64;
const PROGRAM_HEADER_SIZE: u16 = 56;
const SECTION_HEADER_SIZE: u16 = 64;
const MIN_PAGE_SIZE: u64 = 4096;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct ElfLoadOptions {
    pub load_base: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ElfLoadResult {
    pub entry: u64,
    pub file_type: ElfFileType,
    pub load_base: u64,
    pub interpreter: Option<String>,
    pub segments: Vec<LoadedSegment>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ElfFileType {
    Executable,
    Dynamic,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LoadedSegment {
    pub vaddr: u64,
    pub mem_size: u64,
    pub file_size: u64,
    pub permissions: SegmentPermissions,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SegmentPermissions {
    pub read: bool,
    pub write: bool,
    pub execute: bool,
}

impl SegmentPermissions {
    fn from_elf_flags(flags: u32) -> Self {
        Self {
            read: (flags & PF_R) != 0,
            write: (flags & PF_W) != 0,
            execute: (flags & PF_X) != 0,
        }
    }
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum ElfLoadError {
    #[error("ELF file is smaller than the ELF64 header")]
    TruncatedHeader,
    #[error("ELF magic is invalid")]
    InvalidMagic,
    #[error("unsupported ELF class {0}")]
    UnsupportedClass(u8),
    #[error("unsupported ELF data encoding {0}")]
    UnsupportedDataEncoding(u8),
    #[error("unsupported ELF version {0}")]
    UnsupportedVersion(u8),
    #[error("unsupported ELF header version {0}")]
    UnsupportedHeaderVersion(u32),
    #[error("unsupported ELF OS ABI {0}")]
    UnsupportedOsAbi(u8),
    #[error("unsupported ELF ABI version {0}")]
    UnsupportedAbiVersion(u8),
    #[error("unsupported ELF file type {0:#x}")]
    UnsupportedFileType(u16),
    #[error("unsupported ELF machine {0:#x}")]
    UnsupportedMachine(u16),
    #[error("ELF e_flags must be zero, got {0:#x}")]
    NonZeroFlags(u32),
    #[error("ELF header size must be 64, got {0}")]
    InvalidHeaderSize(u16),
    #[error("ELF program header entry size must be 56, got {0}")]
    InvalidProgramHeaderSize(u16),
    #[error("ELF section header entry size must be 64, got {0}")]
    InvalidSectionHeaderSize(u16),
    #[error("program header table is out of range")]
    ProgramHeaderTableOutOfRange,
    #[error("program header {index} has unsupported type {p_type:#x}")]
    UnsupportedProgramHeader { index: u16, p_type: u32 },
    #[error("program header {index} file range is out of range")]
    SegmentFileRangeOutOfRange { index: u16 },
    #[error("program header {index} has p_memsz smaller than p_filesz")]
    SegmentMemSizeSmallerThanFileSize { index: u16 },
    #[error("program header {index} has invalid PT_LOAD alignment {align}")]
    InvalidLoadAlignment { index: u16, align: u64 },
    #[error("program header {index} has invalid PT_LOAD flags {flags:#x}")]
    InvalidLoadFlags { index: u16, flags: u32 },
    #[error("program header {index} load address overflows")]
    LoadAddressOverflow { index: u16 },
    #[error("program header {index} PT_INTERP is not valid UTF-8")]
    InvalidInterpreterString { index: u16 },
    #[error("bus error while loading ELF: {0}")]
    Bus(#[from] BusError),
}

#[derive(Debug, Clone, Copy)]
struct ElfHeader {
    file_type: u16,
    version: u32,
    entry: u64,
    phoff: u64,
    flags: u32,
    ehsize: u16,
    phentsize: u16,
    phnum: u16,
    shentsize: u16,
}

#[derive(Debug, Clone, Copy)]
struct ProgramHeader {
    p_type: u32,
    flags: u32,
    offset: u64,
    vaddr: u64,
    file_size: u64,
    mem_size: u64,
    align: u64,
}

pub fn load_elf(
    board: &mut Board,
    bytes: &[u8],
    options: ElfLoadOptions,
) -> Result<ElfLoadResult, ElfLoadError> {
    let header = parse_header(bytes)?;
    validate_header(&header)?;

    let file_type = match header.file_type {
        ET_EXEC => ElfFileType::Executable,
        ET_DYN => ElfFileType::Dynamic,
        other => return Err(ElfLoadError::UnsupportedFileType(other)),
    };

    let entry = match file_type {
        ElfFileType::Executable => header.entry,
        ElfFileType::Dynamic => options
            .load_base
            .checked_add(header.entry)
            .ok_or(ElfLoadError::LoadAddressOverflow { index: u16::MAX })?,
    };

    let program_headers = parse_program_headers(bytes, &header)?;
    let mut segments = Vec::new();
    let mut interpreter = None;

    for (index, program_header) in program_headers.iter().copied().enumerate() {
        let index = index as u16;
        match program_header.p_type {
            PT_NULL | PT_DYNAMIC | PT_NOTE | PT_PHDR | PT_TLS | PT_GNU_STACK => {}
            PT_INTERP => {
                interpreter = Some(read_interp(bytes, index, &program_header)?);
            }
            PT_LOAD => {
                validate_load_segment(index, &program_header, bytes)?;
                let load_addr =
                    segment_load_addr(index, file_type, options.load_base, &program_header)?;
                load_segment(board, index, load_addr, &program_header, bytes)?;
                segments.push(LoadedSegment {
                    vaddr: load_addr,
                    mem_size: program_header.mem_size,
                    file_size: program_header.file_size,
                    permissions: SegmentPermissions::from_elf_flags(program_header.flags),
                });
            }
            other => {
                return Err(ElfLoadError::UnsupportedProgramHeader {
                    index,
                    p_type: other,
                });
            }
        }
    }

    Ok(ElfLoadResult {
        entry,
        file_type,
        load_base: options.load_base,
        interpreter,
        segments,
    })
}

fn parse_header(bytes: &[u8]) -> Result<ElfHeader, ElfLoadError> {
    if bytes.len() < ELF_HEADER_SIZE as usize {
        return Err(ElfLoadError::TruncatedHeader);
    }

    if &bytes[0..4] != b"\x7fELF" {
        return Err(ElfLoadError::InvalidMagic);
    }
    if bytes[EI_CLASS] != ELFCLASS64 {
        return Err(ElfLoadError::UnsupportedClass(bytes[EI_CLASS]));
    }
    if bytes[EI_DATA] != ELFDATA2LSB {
        return Err(ElfLoadError::UnsupportedDataEncoding(bytes[EI_DATA]));
    }
    if bytes[EI_VERSION] != EV_CURRENT {
        return Err(ElfLoadError::UnsupportedVersion(bytes[EI_VERSION]));
    }
    if bytes[EI_OSABI] != ELFOSABI_NONE {
        return Err(ElfLoadError::UnsupportedOsAbi(bytes[EI_OSABI]));
    }
    if bytes[EI_ABIVERSION] != 0 {
        return Err(ElfLoadError::UnsupportedAbiVersion(bytes[EI_ABIVERSION]));
    }

    let machine = read_u16(bytes, 18);
    if machine != EM_BEDROCK {
        return Err(ElfLoadError::UnsupportedMachine(machine));
    }

    Ok(ElfHeader {
        file_type: read_u16(bytes, 16),
        version: read_u32(bytes, 20),
        entry: read_u64(bytes, 24),
        phoff: read_u64(bytes, 32),
        flags: read_u32(bytes, 48),
        ehsize: read_u16(bytes, 52),
        phentsize: read_u16(bytes, 54),
        phnum: read_u16(bytes, 56),
        shentsize: read_u16(bytes, 58),
    })
}

fn validate_header(header: &ElfHeader) -> Result<(), ElfLoadError> {
    if header.version != EV_CURRENT as u32 {
        return Err(ElfLoadError::UnsupportedHeaderVersion(header.version));
    }
    if header.flags != 0 {
        return Err(ElfLoadError::NonZeroFlags(header.flags));
    }
    if header.ehsize != ELF_HEADER_SIZE {
        return Err(ElfLoadError::InvalidHeaderSize(header.ehsize));
    }
    if header.phentsize != PROGRAM_HEADER_SIZE {
        return Err(ElfLoadError::InvalidProgramHeaderSize(header.phentsize));
    }
    if header.shentsize != SECTION_HEADER_SIZE {
        return Err(ElfLoadError::InvalidSectionHeaderSize(header.shentsize));
    }
    Ok(())
}

fn parse_program_headers(
    bytes: &[u8],
    header: &ElfHeader,
) -> Result<Vec<ProgramHeader>, ElfLoadError> {
    let phoff =
        usize::try_from(header.phoff).map_err(|_| ElfLoadError::ProgramHeaderTableOutOfRange)?;
    let phentsize = header.phentsize as usize;
    let phnum = header.phnum as usize;
    let table_size = phentsize
        .checked_mul(phnum)
        .ok_or(ElfLoadError::ProgramHeaderTableOutOfRange)?;
    let table_end = phoff
        .checked_add(table_size)
        .ok_or(ElfLoadError::ProgramHeaderTableOutOfRange)?;

    if table_end > bytes.len() {
        return Err(ElfLoadError::ProgramHeaderTableOutOfRange);
    }

    let mut program_headers = Vec::with_capacity(phnum);
    for index in 0..phnum {
        let offset = phoff + index * phentsize;
        program_headers.push(ProgramHeader {
            p_type: read_u32(bytes, offset),
            flags: read_u32(bytes, offset + 4),
            offset: read_u64(bytes, offset + 8),
            vaddr: read_u64(bytes, offset + 16),
            file_size: read_u64(bytes, offset + 32),
            mem_size: read_u64(bytes, offset + 40),
            align: read_u64(bytes, offset + 48),
        });
    }

    Ok(program_headers)
}

fn validate_load_segment(
    index: u16,
    program_header: &ProgramHeader,
    bytes: &[u8],
) -> Result<(), ElfLoadError> {
    if program_header.mem_size < program_header.file_size {
        return Err(ElfLoadError::SegmentMemSizeSmallerThanFileSize { index });
    }
    if program_header.align < MIN_PAGE_SIZE {
        return Err(ElfLoadError::InvalidLoadAlignment {
            index,
            align: program_header.align,
        });
    }
    if (program_header.flags & !(PF_R | PF_W | PF_X)) != 0 || (program_header.flags & PF_R) == 0 {
        return Err(ElfLoadError::InvalidLoadFlags {
            index,
            flags: program_header.flags,
        });
    }

    let file_start = usize::try_from(program_header.offset)
        .map_err(|_| ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    let file_size = usize::try_from(program_header.file_size)
        .map_err(|_| ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    let file_end = file_start
        .checked_add(file_size)
        .ok_or(ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    if file_end > bytes.len() {
        return Err(ElfLoadError::SegmentFileRangeOutOfRange { index });
    }

    Ok(())
}

fn segment_load_addr(
    index: u16,
    file_type: ElfFileType,
    load_base: u64,
    program_header: &ProgramHeader,
) -> Result<u64, ElfLoadError> {
    match file_type {
        ElfFileType::Executable => Ok(program_header.vaddr),
        ElfFileType::Dynamic => load_base
            .checked_add(program_header.vaddr)
            .ok_or(ElfLoadError::LoadAddressOverflow { index }),
    }
}

fn load_segment(
    board: &mut Board,
    index: u16,
    load_addr: u64,
    program_header: &ProgramHeader,
    bytes: &[u8],
) -> Result<(), ElfLoadError> {
    let file_start = usize::try_from(program_header.offset)
        .map_err(|_| ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    let file_size = usize::try_from(program_header.file_size)
        .map_err(|_| ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    let file_end = file_start + file_size;

    for (offset, value) in bytes[file_start..file_end].iter().copied().enumerate() {
        let addr = load_addr
            .checked_add(offset as u64)
            .ok_or(ElfLoadError::LoadAddressOverflow { index })?;
        board.write_u8(addr, value)?;
    }

    for offset in program_header.file_size..program_header.mem_size {
        let addr = load_addr
            .checked_add(offset)
            .ok_or(ElfLoadError::LoadAddressOverflow { index })?;
        board.write_u8(addr, 0)?;
    }

    Ok(())
}

fn read_interp(
    bytes: &[u8],
    index: u16,
    program_header: &ProgramHeader,
) -> Result<String, ElfLoadError> {
    let file_start = usize::try_from(program_header.offset)
        .map_err(|_| ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    let file_size = usize::try_from(program_header.file_size)
        .map_err(|_| ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    let file_end = file_start
        .checked_add(file_size)
        .ok_or(ElfLoadError::SegmentFileRangeOutOfRange { index })?;
    if file_end > bytes.len() {
        return Err(ElfLoadError::SegmentFileRangeOutOfRange { index });
    }

    let raw = &bytes[file_start..file_end];
    let end = raw.iter().position(|byte| *byte == 0).unwrap_or(raw.len());
    String::from_utf8(raw[..end].to_vec())
        .map_err(|_| ElfLoadError::InvalidInterpreterString { index })
}

fn read_u16(bytes: &[u8], offset: usize) -> u16 {
    u16::from_le_bytes(
        bytes[offset..offset + 2]
            .try_into()
            .expect("validated range"),
    )
}

fn read_u32(bytes: &[u8], offset: usize) -> u32 {
    u32::from_le_bytes(
        bytes[offset..offset + 4]
            .try_into()
            .expect("validated range"),
    )
}

fn read_u64(bytes: &[u8], offset: usize) -> u64 {
    u64::from_le_bytes(
        bytes[offset..offset + 8]
            .try_into()
            .expect("validated range"),
    )
}

#[cfg(test)]
mod tests {
    use super::{
        EM_BEDROCK, ET_DYN, ET_EXEC, ElfFileType, ElfLoadError, ElfLoadOptions, PF_R, PF_X,
        load_elf,
    };
    use crate::Board;
    use bedrock_bus::Bus;

    #[test]
    fn loads_executable_load_segment_and_zero_fills_bss() {
        let mut board = Board::new();
        let elf = test_elf(ET_EXEC, EM_BEDROCK, 0x210, 0x200, &[0xaa, 0xbb, 0xcc], 8);

        let result = load_elf(&mut board, &elf, ElfLoadOptions::default()).unwrap();

        assert_eq!(result.file_type, ElfFileType::Executable);
        assert_eq!(result.entry, 0x210);
        assert_eq!(result.segments.len(), 1);
        assert_eq!(board.read_u8(0x200).unwrap(), 0xaa);
        assert_eq!(board.read_u8(0x201).unwrap(), 0xbb);
        assert_eq!(board.read_u8(0x202).unwrap(), 0xcc);
        assert_eq!(board.read_u8(0x203).unwrap(), 0);
        assert_eq!(board.read_u8(0x207).unwrap(), 0);
    }

    #[test]
    fn applies_load_base_to_dynamic_entry_and_segments() {
        let mut board = Board::new();
        let elf = test_elf(ET_DYN, EM_BEDROCK, 0x10, 0x20, &[0x5a], 1);

        let result = load_elf(&mut board, &elf, ElfLoadOptions { load_base: 0x4000 }).unwrap();

        assert_eq!(result.file_type, ElfFileType::Dynamic);
        assert_eq!(result.entry, 0x4010);
        assert_eq!(result.segments[0].vaddr, 0x4020);
        assert_eq!(board.read_u8(0x4020).unwrap(), 0x5a);
    }

    #[test]
    fn rejects_non_bedrock_machine() {
        let mut board = Board::new();
        let elf = test_elf(ET_EXEC, 0x003e, 0, 0, &[], 0);

        assert_eq!(
            load_elf(&mut board, &elf, ElfLoadOptions::default()).unwrap_err(),
            ElfLoadError::UnsupportedMachine(0x003e)
        );
    }

    fn test_elf(
        file_type: u16,
        machine: u16,
        entry: u64,
        vaddr: u64,
        data: &[u8],
        mem_size: u64,
    ) -> Vec<u8> {
        let data_offset = 0x100usize;
        let mut bytes = vec![0; data_offset + data.len()];
        bytes[0..4].copy_from_slice(b"\x7fELF");
        bytes[4] = 2;
        bytes[5] = 1;
        bytes[6] = 1;
        bytes[7] = 0;
        bytes[8] = 0;

        write_u16(&mut bytes, 16, file_type);
        write_u16(&mut bytes, 18, machine);
        write_u32(&mut bytes, 20, 1);
        write_u64(&mut bytes, 24, entry);
        write_u64(&mut bytes, 32, 64);
        write_u32(&mut bytes, 48, 0);
        write_u16(&mut bytes, 52, 64);
        write_u16(&mut bytes, 54, 56);
        write_u16(&mut bytes, 56, 1);
        write_u16(&mut bytes, 58, 64);

        write_u32(&mut bytes, 64, 1);
        write_u32(&mut bytes, 68, PF_R | PF_X);
        write_u64(&mut bytes, 72, data_offset as u64);
        write_u64(&mut bytes, 80, vaddr);
        write_u64(&mut bytes, 96, data.len() as u64);
        write_u64(&mut bytes, 104, mem_size);
        write_u64(&mut bytes, 112, 4096);
        bytes[data_offset..data_offset + data.len()].copy_from_slice(data);
        bytes
    }

    fn write_u16(bytes: &mut [u8], offset: usize, value: u16) {
        bytes[offset..offset + 2].copy_from_slice(&value.to_le_bytes());
    }

    fn write_u32(bytes: &mut [u8], offset: usize, value: u32) {
        bytes[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
    }

    fn write_u64(bytes: &mut [u8], offset: usize, value: u64) {
        bytes[offset..offset + 8].copy_from_slice(&value.to_le_bytes());
    }
}
