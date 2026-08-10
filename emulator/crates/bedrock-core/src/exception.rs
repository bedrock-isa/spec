//! Pure architectural event and event-frame definitions.
//!
//! This module deliberately contains no CPU or memory mutation.  It is the
//! common validation boundary used by event entry and by ERET before either
//! path performs its single architectural commit.

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct EventControl(u64);

impl EventControl {
    const WRITABLE_MASK: u64 = (0x0f << 8) | 1;
    const NMI_PENDING: u64 = 1 << 7;
    const IMAGE_MASK: u64 = Self::WRITABLE_MASK | Self::NMI_PENDING;

    pub const fn from_raw(raw: u64) -> Self {
        Self(raw)
    }

    pub const fn raw(self) -> u64 {
        self.0
    }

    pub const fn valid(self) -> bool {
        self.0 & 1 != 0
    }

    pub const fn nmi_pending(self) -> bool {
        self.0 & Self::NMI_PENDING != 0
    }

    pub const fn max_event_depth(self) -> u8 {
        ((self.0 >> 8) & 0x0f) as u8
    }

    /// ECR writes cannot supply the hardware-managed pending-NMI latch.
    pub const fn with_software_write(self, raw: u64) -> Self {
        Self((self.0 & Self::NMI_PENDING) | (raw & Self::WRITABLE_MASK))
    }

    /// Checks a software-supplied ECR image, while preserving the hardware
    /// owned NMI pending latch from the current register image.
    pub const fn validate_software_image(self, raw: u64) -> Result<Self, InvalidControlCause> {
        if raw & !Self::IMAGE_MASK != 0 {
            Err(InvalidControlCause::ReservedBits)
        } else {
            Ok(self.with_software_write(raw))
        }
    }

    pub const fn with_nmi_pending(self, pending: bool) -> Self {
        if pending {
            Self(self.0 | Self::NMI_PENDING)
        } else {
            Self(self.0 & !Self::NMI_PENDING)
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum ExceptionFrameType {
    Basic = 0,
    Error = 1,
    PageFault = 2,
    Auxiliary = 3,
}

impl ExceptionFrameType {
    pub const fn from_raw(raw: u8) -> Option<Self> {
        match raw {
            0 => Some(Self::Basic),
            1 => Some(Self::Error),
            2 => Some(Self::PageFault),
            3 => Some(Self::Auxiliary),
            _ => None,
        }
    }

    pub const fn raw(self) -> u8 {
        self as u8
    }

    pub const fn slots(self) -> u8 {
        match self {
            Self::Basic => 8,
            Self::Error => 10,
            Self::PageFault | Self::Auxiliary => 12,
        }
    }

    pub const fn bytes(self) -> u16 {
        self.slots() as u16 * 8
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum EventClass {
    Exception = 0,
    Interrupt = 1,
    Nmi = 2,
}

impl EventClass {
    pub const fn from_raw(raw: u8) -> Option<Self> {
        match raw {
            0 => Some(Self::Exception),
            1 => Some(Self::Interrupt),
            2 => Some(Self::Nmi),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u32)]
pub enum BaseException {
    DebugTrace = 0x00,
    Breakpoint = 0x02,
    IllegalInstruction = 0x03,
    PrivilegeFault = 0x08,
    PageFault = 0x09,
    DivideError = 0x0a,
    InvalidControlState = 0x0d,
    FloatingPointFault = 0x0e,
    DoubleFault = 0x18,
    MachineCheck = 0x19,
    BusError = 0x1a,
}

impl BaseException {
    pub const fn from_id(id: u32) -> Option<Self> {
        match id {
            0x00 => Some(Self::DebugTrace),
            0x02 => Some(Self::Breakpoint),
            0x03 => Some(Self::IllegalInstruction),
            0x08 => Some(Self::PrivilegeFault),
            0x09 => Some(Self::PageFault),
            0x0a => Some(Self::DivideError),
            0x0d => Some(Self::InvalidControlState),
            0x0e => Some(Self::FloatingPointFault),
            0x18 => Some(Self::DoubleFault),
            0x19 => Some(Self::MachineCheck),
            0x1a => Some(Self::BusError),
            _ => None,
        }
    }

    pub const fn frame_type(self) -> ExceptionFrameType {
        match self {
            Self::DebugTrace | Self::Breakpoint | Self::PrivilegeFault => ExceptionFrameType::Basic,
            Self::IllegalInstruction
            | Self::DivideError
            | Self::InvalidControlState
            | Self::FloatingPointFault => ExceptionFrameType::Error,
            Self::PageFault => ExceptionFrameType::PageFault,
            Self::DoubleFault | Self::MachineCheck | Self::BusError => {
                ExceptionFrameType::Auxiliary
            }
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EventCode(u32);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EventFrameDescriptor {
    pub frame_type: ExceptionFrameType,
    pub slots: u8,
}

impl EventFrameDescriptor {
    pub const fn new(frame_type: ExceptionFrameType) -> Self {
        Self {
            frame_type,
            slots: frame_type.slots(),
        }
    }
}

impl EventCode {
    pub const fn new(class: EventClass, id: u32) -> Option<Self> {
        if id <= 0x00ff_ffff {
            Some(Self(((class as u32) << 24) | id))
        } else {
            None
        }
    }

    pub const fn exception(exception: BaseException) -> Self {
        Self(exception as u32)
    }

    pub const fn from_raw(raw: u32) -> Self {
        Self(raw)
    }

    pub const fn raw(self) -> u32 {
        self.0
    }

    pub const fn class(self) -> Option<EventClass> {
        EventClass::from_raw((self.0 >> 24) as u8)
    }

    pub const fn id(self) -> u32 {
        self.0 & 0x00ff_ffff
    }

    pub const fn base_exception(self) -> Option<BaseException> {
        match self.class() {
            Some(EventClass::Exception) => BaseException::from_id(self.id()),
            _ => None,
        }
    }

    pub const fn frame_type(self) -> Option<ExceptionFrameType> {
        match self.class() {
            Some(EventClass::Exception) => match BaseException::from_id(self.id()) {
                Some(exception) => Some(exception.frame_type()),
                None => None,
            },
            Some(EventClass::Interrupt) | Some(EventClass::Nmi) => Some(ExceptionFrameType::Basic),
            None => None,
        }
    }

    pub const fn frame_descriptor(self) -> Option<EventFrameDescriptor> {
        match self.frame_type() {
            Some(frame_type) => Some(EventFrameDescriptor::new(frame_type)),
            None => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum InvalidControlCause {
    InvalidSelector = 0,
    ReservedBits = 1,
    InvalidImage = 2,
    InvalidTransition = 3,
}

impl InvalidControlCause {
    pub const fn from_raw(raw: u8) -> Option<Self> {
        match raw {
            0 => Some(Self::InvalidSelector),
            1 => Some(Self::ReservedBits),
            2 => Some(Self::InvalidImage),
            3 => Some(Self::InvalidTransition),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FrameControl {
    pub frame_type: ExceptionFrameType,
    pub saved_edepth: u8,
    pub saved_esl: u8,
    pub repeat_saved: bool,
    pub flags: u16,
    pub status: u16,
}

impl FrameControl {
    const RESERVED_MASK: u64 = 0x0000_0000_fff8_0000;
    const FLAGS_MASK: u16 = 0x000f;
    const STATUS_MASK: u16 = 0x003f;

    pub const fn new(
        frame_type: ExceptionFrameType,
        saved_edepth: u8,
        saved_esl: u8,
        repeat_saved: bool,
        flags: u16,
        status: u16,
    ) -> Result<Self, InvalidControlCause> {
        let value = Self {
            frame_type,
            saved_edepth,
            saved_esl,
            repeat_saved,
            flags,
            status,
        };
        match value.validate_fields() {
            Some(cause) => Err(cause),
            None => Ok(value),
        }
    }

    pub const fn frame_size(self) -> u8 {
        self.frame_type.slots()
    }

    pub const fn encode(self) -> u64 {
        (self.frame_size() as u64)
            | ((self.frame_type.raw() as u64) << 8)
            | ((self.saved_edepth as u64) << 12)
            | ((self.saved_esl as u64) << 16)
            | ((self.repeat_saved as u64) << 18)
            | ((self.flags as u64) << 32)
            | ((self.status as u64) << 48)
    }

    pub const fn decode(raw: u64) -> Result<Self, InvalidControlCause> {
        if raw & Self::RESERVED_MASK != 0 {
            return Err(InvalidControlCause::ReservedBits);
        }
        let Some(frame_type) = ExceptionFrameType::from_raw(((raw >> 8) & 0x0f) as u8) else {
            return Err(InvalidControlCause::InvalidImage);
        };
        if (raw & 0xff) as u8 != frame_type.slots() {
            return Err(InvalidControlCause::InvalidImage);
        }
        Self::new(
            frame_type,
            ((raw >> 12) & 0x0f) as u8,
            ((raw >> 16) & 0x03) as u8,
            raw & (1 << 18) != 0,
            (raw >> 32) as u16,
            (raw >> 48) as u16,
        )
    }

    const fn validate_fields(self) -> Option<InvalidControlCause> {
        if self.saved_edepth > 15 || self.saved_esl > 3 {
            return Some(InvalidControlCause::InvalidImage);
        }
        if self.flags & !Self::FLAGS_MASK != 0 || self.status & !Self::STATUS_MASK != 0 {
            return Some(InvalidControlCause::ReservedBits);
        }
        None
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EventInfo(EventCode);

impl EventInfo {
    pub const fn new(event_code: EventCode) -> Self {
        Self(event_code)
    }

    pub const fn event_code(self) -> EventCode {
        self.0
    }

    pub const fn encode(self) -> u64 {
        self.0.raw() as u64
    }

    pub const fn decode(raw: u64) -> Result<Self, InvalidControlCause> {
        if raw >> 32 != 0 {
            return Err(InvalidControlCause::ReservedBits);
        }
        Ok(Self(EventCode::from_raw(raw as u32)))
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum RepeatKind {
    Scalar = 0,
    Group = 1,
}

impl RepeatKind {
    const fn from_raw(raw: u8) -> Option<Self> {
        match raw {
            0 => Some(Self::Scalar),
            1 => Some(Self::Group),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RepeatContinuation {
    pub register: u8,
    pub condition: u8,
    pub kind: RepeatKind,
    pub group_start_delta: u16,
    pub body_bytes: u16,
}

impl RepeatContinuation {
    const RESERVED_MASK: u64 = 0xffff_0000_0000_fc00;
    const CONDITION_TRUE: u8 = 0;

    pub const fn new(
        register: u8,
        condition: u8,
        kind: RepeatKind,
        group_start_delta: u16,
        body_bytes: u16,
    ) -> Result<Self, InvalidControlCause> {
        let value = Self {
            register,
            condition,
            kind,
            group_start_delta,
            body_bytes,
        };
        match value.validate_fields() {
            Some(cause) => Err(cause),
            None => Ok(value),
        }
    }

    pub const fn encode(self) -> u64 {
        (self.register as u64)
            | ((self.condition as u64) << 4)
            | ((self.kind as u64) << 8)
            | ((self.group_start_delta as u64) << 16)
            | ((self.body_bytes as u64) << 32)
    }

    pub const fn decode(raw: u64) -> Result<Self, InvalidControlCause> {
        if raw & Self::RESERVED_MASK != 0 {
            return Err(InvalidControlCause::ReservedBits);
        }
        let Some(kind) = RepeatKind::from_raw(((raw >> 8) & 0x03) as u8) else {
            return Err(InvalidControlCause::InvalidImage);
        };
        Self::new(
            (raw & 0x0f) as u8,
            ((raw >> 4) & 0x0f) as u8,
            kind,
            ((raw >> 16) & 0xffff) as u16,
            ((raw >> 32) & 0xffff) as u16,
        )
    }

    const fn validate_fields(self) -> Option<InvalidControlCause> {
        if self.register > 15 || self.condition > 15 || self.condition == 1 {
            return Some(InvalidControlCause::InvalidImage);
        }
        match self.kind {
            RepeatKind::Scalar => {
                if self.group_start_delta != 0 || self.body_bytes != 0 {
                    return Some(InvalidControlCause::InvalidImage);
                }
            }
            RepeatKind::Group => {
                if self.condition != Self::CONDITION_TRUE || self.body_bytes == 0 {
                    return Some(InvalidControlCause::InvalidImage);
                }
            }
        }
        None
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EventFrameMetadata {
    pub control: FrameControl,
    pub info: EventInfo,
    pub repeat: Option<RepeatContinuation>,
}

impl EventFrameMetadata {
    pub const fn new(
        control: FrameControl,
        info: EventInfo,
        repeat: Option<RepeatContinuation>,
    ) -> Self {
        Self {
            control,
            info,
            repeat,
        }
    }

    /// Decodes the three frame words that ERET must validate before restoring
    /// any architectural state.
    pub const fn decode_return_frame(
        frame_control: u64,
        event_info: u64,
        frame_ext1: u64,
    ) -> Result<Self, InvalidControlCause> {
        let control = match FrameControl::decode(frame_control) {
            Ok(control) => control,
            Err(cause) => return Err(cause),
        };
        let info = match EventInfo::decode(event_info) {
            Ok(info) => info,
            Err(cause) => return Err(cause),
        };
        let repeat = if control.repeat_saved {
            match RepeatContinuation::decode(frame_ext1) {
                Ok(repeat) => Some(repeat),
                Err(cause) => return Err(cause),
            }
        } else {
            if frame_ext1 != 0 {
                return Err(InvalidControlCause::InvalidImage);
            }
            None
        };
        Ok(Self::new(control, info, repeat))
    }

    /// Validates the complete frame shape before ERET restores any state.
    pub fn validate_for_eret(
        self,
        current_edepth: u8,
        current_esl: u8,
    ) -> Result<(), InvalidControlCause> {
        if let Some(cause) = self.control.validate_fields() {
            return Err(cause);
        }
        let Some(required_type) = self.info.event_code().frame_type() else {
            return Err(InvalidControlCause::InvalidImage);
        };
        if required_type as u8 != self.control.frame_type as u8 {
            return Err(InvalidControlCause::InvalidImage);
        }
        if self.control.saved_edepth.checked_add(1) != Some(current_edepth)
            || self.control.saved_esl > current_esl
        {
            return Err(InvalidControlCause::InvalidTransition);
        }
        let saved_event_active = self.control.status & 1 != 0;
        if !saved_event_active && (self.control.saved_edepth != 0 || self.control.saved_esl != 0) {
            return Err(InvalidControlCause::InvalidImage);
        }
        match (self.control.repeat_saved, self.repeat) {
            (true, Some(repeat)) => match repeat.validate_fields() {
                Some(cause) => Err(cause),
                None => Ok(()),
            },
            (false, None) => Ok(()),
            _ => Err(InvalidControlCause::InvalidImage),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn event_descriptors_cover_every_assigned_base_exception() {
        let cases = [
            (BaseException::DebugTrace, ExceptionFrameType::Basic),
            (BaseException::Breakpoint, ExceptionFrameType::Basic),
            (BaseException::IllegalInstruction, ExceptionFrameType::Error),
            (BaseException::PrivilegeFault, ExceptionFrameType::Basic),
            (BaseException::PageFault, ExceptionFrameType::PageFault),
            (BaseException::DivideError, ExceptionFrameType::Error),
            (
                BaseException::InvalidControlState,
                ExceptionFrameType::Error,
            ),
            (BaseException::FloatingPointFault, ExceptionFrameType::Error),
            (BaseException::DoubleFault, ExceptionFrameType::Auxiliary),
            (BaseException::MachineCheck, ExceptionFrameType::Auxiliary),
            (BaseException::BusError, ExceptionFrameType::Auxiliary),
        ];
        for (exception, frame_type) in cases {
            let code = EventCode::exception(exception);
            assert_eq!(code.frame_type(), Some(frame_type));
            assert_eq!(
                code.frame_descriptor(),
                Some(EventFrameDescriptor::new(frame_type))
            );
        }
        assert_eq!(EventCode::from_raw(0x0000_0001).frame_descriptor(), None);
        assert_eq!(EventCode::from_raw(0x0300_0000).frame_descriptor(), None);
        for class in [EventClass::Interrupt, EventClass::Nmi] {
            assert_eq!(
                EventCode::new(class, 0x1234).unwrap().frame_descriptor(),
                Some(EventFrameDescriptor::new(ExceptionFrameType::Basic))
            );
        }
    }

    #[test]
    fn frame_type_sizes_and_event_info_round_trip() {
        assert_eq!(ExceptionFrameType::Basic.slots(), 8);
        assert_eq!(ExceptionFrameType::Error.slots(), 10);
        assert_eq!(ExceptionFrameType::PageFault.slots(), 12);
        assert_eq!(ExceptionFrameType::Auxiliary.slots(), 12);
        let code = EventCode::exception(BaseException::FloatingPointFault);
        let info = EventInfo::new(code);
        assert_eq!(EventInfo::decode(info.encode()), Ok(info));
        assert_eq!(
            EventInfo::decode(1u64 << 32),
            Err(InvalidControlCause::ReservedBits)
        );
        assert_eq!(EventCode::from_raw(0x0300_0000).frame_type(), None);
    }

    #[test]
    fn frame_control_rejects_reserved_bits_masks_and_wrong_shape() {
        let control =
            FrameControl::new(ExceptionFrameType::Error, 0, 0, false, 0x0f, 0x3f).unwrap();
        assert_eq!(FrameControl::decode(control.encode()), Ok(control));
        assert_eq!(
            FrameControl::decode(control.encode() | (1 << 19)),
            Err(InvalidControlCause::ReservedBits)
        );
        assert_eq!(
            FrameControl::decode((control.encode() & !0xff) | 8),
            Err(InvalidControlCause::InvalidImage)
        );
        assert_eq!(
            FrameControl::new(ExceptionFrameType::Basic, 0, 0, false, 0x10, 0),
            Err(InvalidControlCause::ReservedBits)
        );
        assert_eq!(
            FrameControl::new(ExceptionFrameType::Basic, 0, 0, false, 0, 0x40),
            Err(InvalidControlCause::ReservedBits)
        );
    }

    #[test]
    fn repeat_round_trips_and_enforces_kind_invariants() {
        let scalar = RepeatContinuation::new(3, 2, RepeatKind::Scalar, 0, 0).unwrap();
        assert_eq!(RepeatContinuation::decode(scalar.encode()), Ok(scalar));
        let group = RepeatContinuation::new(4, 0, RepeatKind::Group, 0, 14).unwrap();
        assert_eq!(RepeatContinuation::decode(group.encode()), Ok(group));
        assert_eq!(
            RepeatContinuation::new(0, 0, RepeatKind::Scalar, 1, 0),
            Err(InvalidControlCause::InvalidImage)
        );
        assert_eq!(
            RepeatContinuation::new(0, 2, RepeatKind::Group, 1, 1),
            Err(InvalidControlCause::InvalidImage)
        );
        assert_eq!(
            RepeatContinuation::new(0, 0, RepeatKind::Group, 0, 0),
            Err(InvalidControlCause::InvalidImage)
        );
        assert_eq!(
            RepeatContinuation::decode(1 << 10),
            Err(InvalidControlCause::ReservedBits)
        );
        assert_eq!(
            RepeatContinuation::decode(2 << 8),
            Err(InvalidControlCause::InvalidImage)
        );
    }

    #[test]
    fn eret_metadata_checks_shape_nesting_event_active_and_repeat_image() {
        let control = FrameControl::new(ExceptionFrameType::Error, 1, 1, true, 0, 1).unwrap();
        let frame = EventFrameMetadata::new(
            control,
            EventInfo::new(EventCode::exception(BaseException::InvalidControlState)),
            Some(RepeatContinuation::new(1, 0, RepeatKind::Group, 4, 8).unwrap()),
        );
        assert_eq!(frame.validate_for_eret(2, 2), Ok(()));
        assert_eq!(
            frame.validate_for_eret(1, 2),
            Err(InvalidControlCause::InvalidTransition)
        );
        assert_eq!(
            frame.validate_for_eret(2, 0),
            Err(InvalidControlCause::InvalidTransition)
        );

        let inactive = EventFrameMetadata::new(
            FrameControl::new(ExceptionFrameType::Basic, 1, 0, false, 0, 0).unwrap(),
            EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
            None,
        );
        assert_eq!(
            inactive.validate_for_eret(2, 1),
            Err(InvalidControlCause::InvalidImage)
        );

        let direct_bypass = EventFrameMetadata::new(
            FrameControl {
                frame_type: ExceptionFrameType::Basic,
                saved_edepth: 0,
                saved_esl: 0,
                repeat_saved: false,
                flags: 0x10,
                status: 0,
            },
            EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
            None,
        );
        assert_eq!(
            direct_bypass.validate_for_eret(1, 0),
            Err(InvalidControlCause::ReservedBits)
        );
    }

    #[test]
    fn raw_return_frame_conditionally_decodes_ext1() {
        let no_repeat = FrameControl::new(ExceptionFrameType::Basic, 0, 0, false, 0, 0)
            .unwrap()
            .encode();
        let info = EventInfo::new(EventCode::exception(BaseException::Breakpoint)).encode();
        assert_eq!(
            EventFrameMetadata::decode_return_frame(no_repeat, info, 0)
                .unwrap()
                .repeat,
            None
        );
        assert_eq!(
            EventFrameMetadata::decode_return_frame(no_repeat, info, 1),
            Err(InvalidControlCause::InvalidImage)
        );

        let repeat_control = FrameControl::new(ExceptionFrameType::Basic, 0, 0, true, 0, 0)
            .unwrap()
            .encode();
        let repeat = RepeatContinuation::new(2, 0, RepeatKind::Group, 0, 4)
            .unwrap()
            .encode();
        assert_eq!(
            EventFrameMetadata::decode_return_frame(repeat_control, info, repeat)
                .unwrap()
                .repeat,
            Some(RepeatContinuation::new(2, 0, RepeatKind::Group, 0, 4).unwrap())
        );
        assert_eq!(
            EventFrameMetadata::decode_return_frame(repeat_control, info, 2 << 8),
            Err(InvalidControlCause::InvalidImage)
        );
    }

    #[test]
    fn event_control_preserves_hardware_pending_bit_on_software_write() {
        let ecr = EventControl::from_raw(1 | (7 << 8)).with_nmi_pending(true);
        let written = ecr.with_software_write(0);
        assert!(!written.valid());
        assert_eq!(written.max_event_depth(), 0);
        assert!(written.nmi_pending());
    }

    #[test]
    fn event_control_validates_software_images_and_ignores_supplied_nmi_pending() {
        let current = EventControl::from_raw(1).with_nmi_pending(true);
        let written = current.validate_software_image((3 << 8) | 1).unwrap();
        assert!(written.valid());
        assert_eq!(written.max_event_depth(), 3);
        assert!(written.nmi_pending());
        let clear_latch_attempt = current
            .validate_software_image((3 << 8) | 1 | (1 << 7))
            .unwrap();
        assert!(clear_latch_attempt.nmi_pending());
        assert_eq!(
            current.validate_software_image(1 << 12),
            Err(InvalidControlCause::ReservedBits)
        );
    }
}
