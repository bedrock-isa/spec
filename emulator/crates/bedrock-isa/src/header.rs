use crate::{EncodingClass, OperatorSpace};
use thiserror::Error;

pub const MAX_INSTRUCTION_BYTES: usize = 18;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct InstructionHeader {
    pub class: EncodingClass,
    pub operator_space: Option<OperatorSpace>,
    pub length_bytes: u8,
    pub opcode_bytes: u8,
    pub payload_bits: u8,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Error)]
pub enum HeaderError {
    #[error("instruction stream is empty")]
    Empty,
    #[error("extended instruction needs its second header byte")]
    NeedSecondByte,
    #[error("encoded instruction length {length} is shorter than its {class:?} opcode")]
    OpcodeDoesNotFit { length: u8, class: EncodingClass },
}

pub fn decode_header(bytes: &[u8]) -> Result<InstructionHeader, HeaderError> {
    let byte0 = *bytes.first().ok_or(HeaderError::Empty)?;
    if byte0 & 0x80 == 0 {
        return Ok(InstructionHeader {
            class: EncodingClass::ExtraShort,
            operator_space: None,
            length_bytes: 1,
            opcode_bytes: 1,
            payload_bits: 7,
        });
    }
    if byte0 & 0xc0 == 0x80 {
        return Ok(InstructionHeader {
            class: EncodingClass::Short,
            operator_space: None,
            length_bytes: 2,
            opcode_bytes: 2,
            payload_bits: 14,
        });
    }

    let byte1 = *bytes.get(1).ok_or(HeaderError::NeedSecondByte)?;
    let length_bytes = 3 + ((byte0 >> 2) & 0x0f);
    let selector = ((byte0 & 0x03) << 4) | (byte1 >> 4);
    let allocation_prefix = ((byte0 & 0x03) << 6) | (byte1 >> 2);
    let class = if selector < 0b111100 {
        EncodingClass::Medium
    } else if selector < 0b111111 {
        EncodingClass::Long
    } else if allocation_prefix == 0xff {
        EncodingClass::Xxlong
    } else {
        EncodingClass::ExtraLong
    };
    if usize::from(length_bytes) < class.opcode_bytes() {
        return Err(HeaderError::OpcodeDoesNotFit {
            length: length_bytes,
            class,
        });
    }
    let prefix = (u16::from(byte0 & 0x03) << 8) | u16::from(byte1);
    let operator_space = match class {
        EncodingClass::ExtraLong | EncodingClass::Xxlong => {
            crate::generated::operator_space_from_prefix(class, prefix)
        }
        EncodingClass::ExtraShort
        | EncodingClass::Short
        | EncodingClass::Medium
        | EncodingClass::Long => None,
    };
    Ok(InstructionHeader {
        class,
        operator_space,
        length_bytes,
        opcode_bytes: class.opcode_bytes() as u8,
        payload_bits: class.payload_bits(),
    })
}

pub fn opcode_payload(header: InstructionHeader, bytes: &[u8]) -> Option<u64> {
    if bytes.len() < usize::from(header.opcode_bytes) {
        return None;
    }
    match header.class {
        EncodingClass::ExtraShort => Some(u64::from(bytes[0] & 0x7f)),
        EncodingClass::Short => Some((u64::from(bytes[0] & 0x3f) << 8) | u64::from(bytes[1])),
        EncodingClass::Medium
        | EncodingClass::Long
        | EncodingClass::ExtraLong
        | EncodingClass::Xxlong => {
            let mut payload = u64::from(bytes[0] & 0x03);
            for byte in &bytes[1..usize::from(header.opcode_bytes)] {
                payload = (payload << 8) | u64::from(*byte);
            }
            Some(payload)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{HeaderError, decode_header, opcode_payload};
    use crate::EncodingClass;

    #[test]
    fn decodes_all_framing_classes() {
        for (bytes, expected_class) in [
            (&[0x01][..], EncodingClass::ExtraShort),
            (&[0x80][..], EncodingClass::Short),
            (&[0xc0, 0x00][..], EncodingClass::Medium),
            (&[0xc7, 0xc0][..], EncodingClass::Long),
            (&[0xcb, 0xf0][..], EncodingClass::ExtraLong),
            (&[0xcf, 0xfc][..], EncodingClass::Xxlong),
        ] {
            let header = decode_header(bytes).unwrap();
            assert_eq!(header.class, expected_class);
            if matches!(
                expected_class,
                EncodingClass::ExtraShort
                    | EncodingClass::Short
                    | EncodingClass::Medium
                    | EncodingClass::Long
            ) {
                assert_eq!(header.operator_space, None);
            }
        }
    }

    #[test]
    fn extracts_short_payload_in_stream_order() {
        let header = decode_header(&[0xaa, 0x55]).unwrap();
        assert_eq!(opcode_payload(header, &[0xaa, 0x55]), Some(0x2a55));
    }

    #[test]
    fn xxlong_requires_six_bytes_and_custom_prefix_stays_extralong() {
        for (byte0, length) in [(0xc3, 3), (0xc7, 4), (0xcb, 5)] {
            assert_eq!(
                decode_header(&[byte0, 0xfc]),
                Err(HeaderError::OpcodeDoesNotFit {
                    length,
                    class: EncodingClass::Xxlong,
                })
            );
        }
        let xxlong = decode_header(&[0xcf, 0xfc]).unwrap();
        assert_eq!(xxlong.class, EncodingClass::Xxlong);
        assert_eq!(xxlong.opcode_bytes, 6);
        assert_eq!(xxlong.payload_bits, 42);
        assert_eq!(
            decode_header(&[0xcb, 0xf8]).unwrap().class,
            EncodingClass::ExtraLong
        );
        assert_eq!(
            decode_header(&[0xcb, 0xf0]).unwrap().class,
            EncodingClass::ExtraLong
        );
    }

    #[test]
    fn operator_space_covers_every_canonical_class_prefix() {
        for &(class, prefix, expected_space) in crate::generated::OPERATOR_SPACE_PREFIX_CASES {
            let opcode_bytes = class.opcode_bytes();
            let length_code = u8::try_from(opcode_bytes - 3).unwrap();
            let byte0 = 0xc0 | (length_code << 2) | ((prefix >> 8) as u8);
            let byte1 = prefix as u8;
            for lower_fill in [0x00, 0xff] {
                let mut bytes = vec![lower_fill; opcode_bytes];
                bytes[0] = byte0;
                bytes[1] = byte1;
                let header = decode_header(&bytes).unwrap();
                assert_eq!(
                    header.class, class,
                    "class={class:?} prefix={prefix:010b} expected={expected_space:?} lower_fill={lower_fill:#04x}"
                );
                assert_eq!(
                    header.operator_space, expected_space,
                    "class={class:?} prefix={prefix:010b} expected={expected_space:?} lower_fill={lower_fill:#04x}"
                );
            }
        }
    }
}
