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
    VectorRangeError = 0x0b,
    InvalidControlState = 0x0d,
    FloatingPointFault = 0x0e,
    DoubleFault = 0x18,
    MachineCheck = 0x19,
    BusError = 0x1a,
    SystemCall = 0x20,
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
            0x0b => Some(Self::VectorRangeError),
            0x0d => Some(Self::InvalidControlState),
            0x0e => Some(Self::FloatingPointFault),
            0x18 => Some(Self::DoubleFault),
            0x19 => Some(Self::MachineCheck),
            0x1a => Some(Self::BusError),
            0x20 => Some(Self::SystemCall),
            _ => None,
        }
    }

    pub const fn frame_type(self) -> ExceptionFrameType {
        match self {
            Self::DebugTrace | Self::Breakpoint | Self::PrivilegeFault | Self::SystemCall => {
                ExceptionFrameType::Basic
            }
            Self::IllegalInstruction
            | Self::DivideError
            | Self::VectorRangeError
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
    pub saved_dfa: bool,
    pub flags: u16,
    pub status: u16,
}

impl FrameControl {
    const RESERVED_MASK: u64 = 0xfff0_0000_ffff_e000;
    const FLAGS_MASK: u16 = 0x000f;
    const STATUS_MASK: u16 = 0x07ff;

    pub const fn new(
        frame_type: ExceptionFrameType,
        saved_dfa: bool,
        flags: u16,
        status: u16,
    ) -> Result<Self, InvalidControlCause> {
        let value = Self {
            frame_type,
            saved_dfa,
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
            | ((if self.saved_dfa { 1 } else { 0 }) << 12)
            | ((self.flags as u64) << 32)
            | ((self.status as u64) << 36)
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
            raw & (1 << 12) != 0,
            ((raw >> 32) & 0x0f) as u16,
            (raw >> 36) as u16,
        )
    }

    const fn validate_fields(self) -> Option<InvalidControlCause> {
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
pub struct EventFrameMetadata {
    pub control: FrameControl,
    pub info: EventInfo,
}

impl EventFrameMetadata {
    pub const fn new(control: FrameControl, info: EventInfo) -> Self {
        Self { control, info }
    }

    /// Decodes the two frame words that ERET must validate before restoring
    /// any architectural state.
    pub const fn decode_return_frame(
        frame_control: u64,
        event_info: u64,
    ) -> Result<Self, InvalidControlCause> {
        let control = match FrameControl::decode(frame_control) {
            Ok(control) => control,
            Err(cause) => return Err(cause),
        };
        let info = match EventInfo::decode(event_info) {
            Ok(info) => info,
            Err(cause) => return Err(cause),
        };
        Ok(Self::new(control, info))
    }

    /// Validates the complete frame shape before ERET restores any state.
    pub fn validate_for_eret(
        self,
        current_edepth: u8,
        current_user_origin: bool,
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
        let saved_edepth = ((self.control.status >> 6) & 0x0f) as u8;
        let saved_user_origin = self.control.status & (1 << 10) != 0;
        let saved_privileged = self.control.status & (1 << 4) != 0;
        if !saved_privileged {
            return Err(InvalidControlCause::InvalidImage);
        }
        if saved_edepth.checked_add(1) != Some(current_edepth)
            || saved_user_origin != current_user_origin
        {
            return Err(InvalidControlCause::InvalidTransition);
        }
        let saved_event_active = self.control.status & 1 != 0;
        if saved_event_active != (saved_edepth != 0)
            || (!saved_event_active && saved_user_origin)
            || (self.control.saved_dfa && !saved_event_active)
        {
            return Err(InvalidControlCause::InvalidImage);
        }
        Ok(())
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
            (BaseException::VectorRangeError, ExceptionFrameType::Error),
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
        let control = FrameControl::new(ExceptionFrameType::Error, false, 0x0f, 0x03f).unwrap();
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
            FrameControl::new(ExceptionFrameType::Basic, false, 0x10, 0),
            Err(InvalidControlCause::ReservedBits)
        );
        assert_eq!(
            FrameControl::new(ExceptionFrameType::Basic, false, 0, 0x0800),
            Err(InvalidControlCause::ReservedBits)
        );
    }

    #[test]
    fn eret_return_frame_decode_rejects_reserved_frame_control_bit_18() {
        let control = FrameControl::new(ExceptionFrameType::Basic, false, 0, 0).unwrap();
        let event_info = EventInfo::new(EventCode::exception(BaseException::Breakpoint));
        assert_eq!(
            EventFrameMetadata::decode_return_frame(
                control.encode() | (1 << 18),
                event_info.encode()
            ),
            Err(InvalidControlCause::ReservedBits)
        );
    }

    #[test]
    fn eret_metadata_checks_shape_nesting_and_event_active() {
        let control = FrameControl::new(ExceptionFrameType::Error, true, 0, 0x0051).unwrap();
        let frame = EventFrameMetadata::new(
            control,
            EventInfo::new(EventCode::exception(BaseException::InvalidControlState)),
        );
        assert_eq!(frame.validate_for_eret(2, false), Ok(()));
        assert_eq!(
            frame.validate_for_eret(1, false),
            Err(InvalidControlCause::InvalidTransition)
        );
        assert_eq!(
            frame.validate_for_eret(2, true),
            Err(InvalidControlCause::InvalidTransition)
        );

        let inactive = EventFrameMetadata::new(
            FrameControl::new(ExceptionFrameType::Basic, false, 0, 0x0040).unwrap(),
            EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
        );
        assert_eq!(
            inactive.validate_for_eret(2, false),
            Err(InvalidControlCause::InvalidImage)
        );

        let active_at_depth_zero = EventFrameMetadata::new(
            FrameControl::new(ExceptionFrameType::Basic, false, 0, 0x0011).unwrap(),
            EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
        );
        assert_eq!(
            active_at_depth_zero.validate_for_eret(1, false),
            Err(InvalidControlCause::InvalidImage)
        );

        let inactive_at_nonzero_depth = EventFrameMetadata::new(
            FrameControl::new(ExceptionFrameType::Basic, false, 0, 0x0050).unwrap(),
            EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
        );
        assert_eq!(
            inactive_at_nonzero_depth.validate_for_eret(2, false),
            Err(InvalidControlCause::InvalidImage)
        );

        let dfa_without_active_event = EventFrameMetadata::new(
            FrameControl::new(ExceptionFrameType::Basic, true, 0, 0x0010).unwrap(),
            EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
        );
        assert_eq!(
            dfa_without_active_event.validate_for_eret(1, false),
            Err(InvalidControlCause::InvalidImage)
        );

        let direct_bypass = EventFrameMetadata::new(
            FrameControl {
                frame_type: ExceptionFrameType::Basic,
                saved_dfa: false,
                flags: 0x10,
                status: 0,
            },
            EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
        );
        assert_eq!(
            direct_bypass.validate_for_eret(1, false),
            Err(InvalidControlCause::ReservedBits)
        );
    }

    #[test]
    fn raw_return_frame_decodes_fixed_metadata() {
        let control = FrameControl::new(ExceptionFrameType::Basic, false, 0, 0)
            .unwrap()
            .encode();
        let info = EventInfo::new(EventCode::exception(BaseException::Breakpoint)).encode();
        assert_eq!(
            EventFrameMetadata::decode_return_frame(control, info),
            Ok(EventFrameMetadata::new(
                FrameControl::new(ExceptionFrameType::Basic, false, 0, 0).unwrap(),
                EventInfo::new(EventCode::exception(BaseException::Breakpoint)),
            ))
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
