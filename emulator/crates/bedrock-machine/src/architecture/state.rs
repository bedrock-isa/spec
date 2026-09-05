use crate::{
    AddressSpaceControl, EventControl, Flags, PageTableControl, SegmentRegister, SegmentRegisters,
    SegmentSelector, Status,
};

/// The emulator selects the architectural minimum MAX_VLEN of 128 bits.
pub const MAX_VLEN_BITS: usize = 128;
pub const MAX_VLEN_BYTES: usize = MAX_VLEN_BITS / 8;
pub const MAX_PREDICATE_BYTES: usize = MAX_VLEN_BYTES / 8;
pub const VECTOR_REGISTER_COUNT: usize = 32;
pub const PREDICATE_REGISTER_COUNT: usize = 16;

pub type VectorRegister = [u8; MAX_VLEN_BYTES];
pub type PredicateRegister = [u8; MAX_PREDICATE_BYTES];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CpuRegisterSet {
    General,
    Link,
    Segment,
    Control,
    FloatingPoint,
    Vector,
}

impl CpuRegisterSet {
    pub const fn label(self) -> &'static str {
        match self {
            Self::General => "General",
            Self::Link => "Link",
            Self::Segment => "Segment",
            Self::Control => "Control",
            Self::FloatingPoint => "FPU",
            Self::Vector => "Vector",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CpuRegister {
    General(usize),
    FloatingPoint(usize),
    Sp,
    Pc,
    Lpc,
    Lpa,
    Flags,
    Status,
    Segment(SegmentSelector),
    Ptcr,
    Ascr,
    Ecr,
    Upc,
    Usp,
    Ucs,
    Uds,
    Uss,
    Uctl,
    Uinfo,
    Epc,
    Ecs,
    Eds,
    Sss,
    Ssp,
    Iss,
    Isp,
    Fss,
    Fsp,
    Dss,
    Dsp,
    BootPc,
    BootCfg,
    Pmc,
    FStatus,
    FFlags,
    VStatus,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CpuRegisterInfo {
    pub name: &'static str,
    pub bits: u16,
    pub set: CpuRegisterSet,
    pub register: CpuRegister,
}

macro_rules! reg {
    ($name:literal, $set:ident, $register:expr) => {
        CpuRegisterInfo {
            name: $name,
            bits: 64,
            set: CpuRegisterSet::$set,
            register: $register,
        }
    };
}

pub const CPU_REGISTER_INFOS: &[CpuRegisterInfo] = &[
    reg!("R0", General, CpuRegister::General(0)),
    reg!("R1", General, CpuRegister::General(1)),
    reg!("R2", General, CpuRegister::General(2)),
    reg!("R3", General, CpuRegister::General(3)),
    reg!("R4", General, CpuRegister::General(4)),
    reg!("R5", General, CpuRegister::General(5)),
    reg!("R6", General, CpuRegister::General(6)),
    reg!("R7", General, CpuRegister::General(7)),
    reg!("R8", General, CpuRegister::General(8)),
    reg!("R9", General, CpuRegister::General(9)),
    reg!("R10", General, CpuRegister::General(10)),
    reg!("R11", General, CpuRegister::General(11)),
    reg!("R12", General, CpuRegister::General(12)),
    reg!("R13", General, CpuRegister::General(13)),
    reg!("R14", General, CpuRegister::General(14)),
    reg!("R15", General, CpuRegister::General(15)),
    reg!("SP", General, CpuRegister::Sp),
    reg!("PC", General, CpuRegister::Pc),
    reg!("LPC", Link, CpuRegister::Lpc),
    reg!("LPA", Link, CpuRegister::Lpa),
    CpuRegisterInfo {
        name: "FLAGS",
        bits: 16,
        set: CpuRegisterSet::General,
        register: CpuRegister::Flags,
    },
    CpuRegisterInfo {
        name: "STATUS",
        bits: 16,
        set: CpuRegisterSet::General,
        register: CpuRegister::Status,
    },
    reg!("CS", Segment, CpuRegister::Segment(SegmentSelector::Cs)),
    reg!("DS", Segment, CpuRegister::Segment(SegmentSelector::Ds)),
    reg!("SS", Segment, CpuRegister::Segment(SegmentSelector::Ss)),
    reg!("GS0", Segment, CpuRegister::Segment(SegmentSelector::Gs0)),
    reg!("GS1", Segment, CpuRegister::Segment(SegmentSelector::Gs1)),
    reg!("GS2", Segment, CpuRegister::Segment(SegmentSelector::Gs2)),
    reg!("GS3", Segment, CpuRegister::Segment(SegmentSelector::Gs3)),
    reg!("GS4", Segment, CpuRegister::Segment(SegmentSelector::Gs4)),
    reg!("GS5", Segment, CpuRegister::Segment(SegmentSelector::Gs5)),
    reg!("PTCR", Control, CpuRegister::Ptcr),
    reg!("ASCR", Control, CpuRegister::Ascr),
    reg!("ECR", Control, CpuRegister::Ecr),
    reg!("UPC", Control, CpuRegister::Upc),
    reg!("USP", Control, CpuRegister::Usp),
    reg!("UCS", Control, CpuRegister::Ucs),
    reg!("UDS", Control, CpuRegister::Uds),
    reg!("USS", Control, CpuRegister::Uss),
    reg!("UCTL", Control, CpuRegister::Uctl),
    reg!("UINFO", Control, CpuRegister::Uinfo),
    reg!("EPC", Control, CpuRegister::Epc),
    reg!("ECS", Control, CpuRegister::Ecs),
    reg!("EDS", Control, CpuRegister::Eds),
    reg!("SSS", Control, CpuRegister::Sss),
    reg!("SSP", Control, CpuRegister::Ssp),
    reg!("ISS", Control, CpuRegister::Iss),
    reg!("ISP", Control, CpuRegister::Isp),
    reg!("FSS", Control, CpuRegister::Fss),
    reg!("FSP", Control, CpuRegister::Fsp),
    reg!("DSS", Control, CpuRegister::Dss),
    reg!("DSP", Control, CpuRegister::Dsp),
    reg!("BOOTPC", Control, CpuRegister::BootPc),
    reg!("BOOTCFG", Control, CpuRegister::BootCfg),
    reg!("PMC", Control, CpuRegister::Pmc),
    reg!("F0", FloatingPoint, CpuRegister::FloatingPoint(0)),
    reg!("F1", FloatingPoint, CpuRegister::FloatingPoint(1)),
    reg!("F2", FloatingPoint, CpuRegister::FloatingPoint(2)),
    reg!("F3", FloatingPoint, CpuRegister::FloatingPoint(3)),
    reg!("F4", FloatingPoint, CpuRegister::FloatingPoint(4)),
    reg!("F5", FloatingPoint, CpuRegister::FloatingPoint(5)),
    reg!("F6", FloatingPoint, CpuRegister::FloatingPoint(6)),
    reg!("F7", FloatingPoint, CpuRegister::FloatingPoint(7)),
    reg!("F8", FloatingPoint, CpuRegister::FloatingPoint(8)),
    reg!("F9", FloatingPoint, CpuRegister::FloatingPoint(9)),
    reg!("F10", FloatingPoint, CpuRegister::FloatingPoint(10)),
    reg!("F11", FloatingPoint, CpuRegister::FloatingPoint(11)),
    reg!("F12", FloatingPoint, CpuRegister::FloatingPoint(12)),
    reg!("F13", FloatingPoint, CpuRegister::FloatingPoint(13)),
    reg!("F14", FloatingPoint, CpuRegister::FloatingPoint(14)),
    reg!("F15", FloatingPoint, CpuRegister::FloatingPoint(15)),
    CpuRegisterInfo {
        name: "FSTATUS",
        bits: 16,
        set: CpuRegisterSet::FloatingPoint,
        register: CpuRegister::FStatus,
    },
    CpuRegisterInfo {
        name: "FFLAGS",
        bits: 16,
        set: CpuRegisterSet::FloatingPoint,
        register: CpuRegister::FFlags,
    },
    CpuRegisterInfo {
        name: "VSTATUS",
        bits: 16,
        set: CpuRegisterSet::Vector,
        register: CpuRegister::VStatus,
    },
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CpuState {
    pub r: [u64; 16],
    pub f: [u64; 16],
    pub v: [VectorRegister; VECTOR_REGISTER_COUNT],
    pub p: [PredicateRegister; PREDICATE_REGISTER_COUNT],
    pub sp: u64,
    pub pc: u64,
    pub lpc: u64,
    pub lpa: u64,
    pub flags: Flags,
    pub status: Status,
    pub segments: SegmentRegisters,
    pub ptcr: PageTableControl,
    pub ascr: AddressSpaceControl,
    pub ecr: EventControl,
    pub upc: u64,
    pub usp: u64,
    pub ucs: SegmentRegister,
    pub uds: SegmentRegister,
    pub uss: SegmentRegister,
    pub uctl: u64,
    pub uinfo: u64,
    pub epc: u64,
    pub ecs: SegmentRegister,
    pub eds: SegmentRegister,
    pub sss: SegmentRegister,
    pub ssp: u64,
    pub iss: SegmentRegister,
    pub isp: u64,
    pub fss: SegmentRegister,
    pub fsp: u64,
    pub dss: SegmentRegister,
    pub dsp: u64,
    pub bootpc: u64,
    pub bootcfg: u64,
    pub pmc: u64,
    pub fstatus: u16,
    pub fflags: u16,
    pub vstatus: u16,
    pub hidden_current_dfa: bool,
}

impl Default for CpuState {
    fn default() -> Self {
        Self {
            r: [0; 16],
            f: [0; 16],
            v: [[0; MAX_VLEN_BYTES]; VECTOR_REGISTER_COUNT],
            p: [[0; MAX_PREDICATE_BYTES]; PREDICATE_REGISTER_COUNT],
            sp: 0,
            pc: 0,
            lpc: 0,
            lpa: 0,
            flags: Flags::empty(),
            status: Status::empty(),
            segments: SegmentRegisters::default(),
            ptcr: PageTableControl::disabled(),
            ascr: AddressSpaceControl::default(),
            ecr: EventControl::default(),
            upc: 0,
            usp: 0,
            ucs: SegmentRegister::disabled(),
            uds: SegmentRegister::disabled(),
            uss: SegmentRegister::disabled(),
            uctl: 0,
            uinfo: 0,
            epc: 0,
            ecs: SegmentRegister::disabled(),
            eds: SegmentRegister::disabled(),
            sss: SegmentRegister::disabled(),
            ssp: 0,
            iss: SegmentRegister::disabled(),
            isp: 0,
            fss: SegmentRegister::disabled(),
            fsp: 0,
            dss: SegmentRegister::disabled(),
            dsp: 0,
            bootpc: 0,
            bootcfg: 0,
            pmc: 0,
            fstatus: 0,
            fflags: 0,
            vstatus: 0,
            hidden_current_dfa: false,
        }
    }
}

impl CpuState {
    pub fn reset(&mut self, pc: u64) {
        *self = Self {
            pc,
            status: Status::PM,
            ..Self::default()
        };
    }
    pub fn read_register(&self, register: CpuRegister) -> u64 {
        match register {
            CpuRegister::General(i) => self.r[i],
            CpuRegister::FloatingPoint(i) => self.f[i],
            CpuRegister::Sp => self.sp,
            CpuRegister::Pc => self.pc,
            CpuRegister::Lpc => self.lpc,
            CpuRegister::Lpa => self.lpa,
            CpuRegister::Flags => u64::from(self.flags.bits()),
            CpuRegister::Status => u64::from(self.status.bits()),
            CpuRegister::Segment(s) => self.segments.get(s).raw(),
            CpuRegister::Ptcr => self.ptcr.raw(),
            CpuRegister::Ascr => self.ascr.raw(),
            CpuRegister::Ecr => self.ecr.raw(),
            CpuRegister::Upc => self.upc,
            CpuRegister::Usp => self.usp,
            CpuRegister::Ucs => self.ucs.raw(),
            CpuRegister::Uds => self.uds.raw(),
            CpuRegister::Uss => self.uss.raw(),
            CpuRegister::Uctl => self.uctl,
            CpuRegister::Uinfo => self.uinfo,
            CpuRegister::Epc => self.epc,
            CpuRegister::Ecs => self.ecs.raw(),
            CpuRegister::Eds => self.eds.raw(),
            CpuRegister::Sss => self.sss.raw(),
            CpuRegister::Ssp => self.ssp,
            CpuRegister::Iss => self.iss.raw(),
            CpuRegister::Isp => self.isp,
            CpuRegister::Fss => self.fss.raw(),
            CpuRegister::Fsp => self.fsp,
            CpuRegister::Dss => self.dss.raw(),
            CpuRegister::Dsp => self.dsp,
            CpuRegister::BootPc => self.bootpc,
            CpuRegister::BootCfg => self.bootcfg,
            CpuRegister::Pmc => self.pmc,
            CpuRegister::FStatus => u64::from(self.fstatus),
            CpuRegister::FFlags => u64::from(self.fflags),
            CpuRegister::VStatus => u64::from(self.vstatus),
        }
    }
    pub fn write_register(&mut self, register: CpuRegister, value: u64) {
        match register {
            CpuRegister::General(i) => self.r[i] = value,
            CpuRegister::FloatingPoint(i) => self.f[i] = value,
            CpuRegister::Sp => self.sp = value,
            CpuRegister::Pc => self.pc = value,
            CpuRegister::Lpc => self.lpc = value,
            CpuRegister::Lpa => self.lpa = value,
            CpuRegister::Flags => self.flags = Flags::from_bits_truncate(value as u16),
            CpuRegister::Status => self.status = Status::from_bits_truncate(value as u16),
            CpuRegister::Segment(s) => self.segments.set(s, SegmentRegister::from_raw(value)),
            CpuRegister::Ptcr => self.ptcr = PageTableControl::from_raw(value),
            CpuRegister::Ascr => self.ascr = AddressSpaceControl::from_raw(value),
            CpuRegister::Ecr => self.ecr = EventControl::from_raw(value),
            CpuRegister::Upc => self.upc = value,
            CpuRegister::Usp => self.usp = value,
            CpuRegister::Ucs => self.ucs = SegmentRegister::from_raw(value),
            CpuRegister::Uds => self.uds = SegmentRegister::from_raw(value),
            CpuRegister::Uss => self.uss = SegmentRegister::from_raw(value),
            CpuRegister::Uctl => self.uctl = value,
            CpuRegister::Uinfo => self.uinfo = value,
            CpuRegister::Epc => self.epc = value,
            CpuRegister::Ecs => self.ecs = SegmentRegister::from_raw(value),
            CpuRegister::Eds => self.eds = SegmentRegister::from_raw(value),
            CpuRegister::Sss => self.sss = SegmentRegister::from_raw(value),
            CpuRegister::Ssp => self.ssp = value,
            CpuRegister::Iss => self.iss = SegmentRegister::from_raw(value),
            CpuRegister::Isp => self.isp = value,
            CpuRegister::Fss => self.fss = SegmentRegister::from_raw(value),
            CpuRegister::Fsp => self.fsp = value,
            CpuRegister::Dss => self.dss = SegmentRegister::from_raw(value),
            CpuRegister::Dsp => self.dsp = value,
            CpuRegister::BootPc => self.bootpc = value,
            CpuRegister::BootCfg => self.bootcfg = value,
            CpuRegister::Pmc => self.pmc = value,
            CpuRegister::FStatus => self.fstatus = value as u16,
            CpuRegister::FFlags => self.fflags = value as u16,
            CpuRegister::VStatus => self.vstatus = value as u16,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reset_clears_all_vector_and_predicate_bits_at_max_vlen() {
        let mut state = CpuState::default();
        state.v[0] = [0xa5; MAX_VLEN_BYTES];
        state.v[VECTOR_REGISTER_COUNT - 1] = [0x5a; MAX_VLEN_BYTES];
        state.p[0] = [0xff; MAX_PREDICATE_BYTES];
        state.p[PREDICATE_REGISTER_COUNT - 1] = [0x81; MAX_PREDICATE_BYTES];

        state.reset(0x1234);

        assert_eq!(state.pc, 0x1234);
        assert_eq!(state.v, [[0; MAX_VLEN_BYTES]; VECTOR_REGISTER_COUNT]);
        assert_eq!(
            state.p,
            [[0; MAX_PREDICATE_BYTES]; PREDICATE_REGISTER_COUNT]
        );
        assert_eq!(MAX_VLEN_BITS, 128);
    }
}
