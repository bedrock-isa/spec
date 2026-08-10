use crate::EncodingClass;
use thiserror::Error;

pub const MAX_INSTRUCTION_BYTES: usize = 18;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct InstructionHeader {
    pub class: EncodingClass,
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
            length_bytes: 1,
            opcode_bytes: 1,
            payload_bits: 7,
        });
    }
    if byte0 & 0xc0 == 0x80 {
        return Ok(InstructionHeader {
            class: EncodingClass::Short,
            length_bytes: 2,
            opcode_bytes: 2,
            payload_bits: 14,
        });
    }

    let byte1 = *bytes.get(1).ok_or(HeaderError::NeedSecondByte)?;
    let length_bytes = 3 + ((byte0 >> 2) & 0x0f);
    let selector = ((byte0 & 0x03) << 4) | (byte1 >> 4);
    let class = if selector < 0b111100 {
        EncodingClass::Medium
    } else if selector < 0b111111 {
        EncodingClass::Long
    } else {
        EncodingClass::ExtraLong
    };
    if usize::from(length_bytes) < class.opcode_bytes() {
        return Err(HeaderError::OpcodeDoesNotFit {
            length: length_bytes,
            class,
        });
    }
    Ok(InstructionHeader {
        class,
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
        EncodingClass::Medium | EncodingClass::Long | EncodingClass::ExtraLong => {
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
    use super::{decode_header, opcode_payload};
    use crate::EncodingClass;

    #[test]
    fn decodes_all_framing_classes() {
        assert_eq!(
            decode_header(&[0x01]).unwrap().class,
            EncodingClass::ExtraShort
        );
        assert_eq!(decode_header(&[0x80]).unwrap().class, EncodingClass::Short);
        assert_eq!(
            decode_header(&[0xc0, 0x00]).unwrap().class,
            EncodingClass::Medium
        );
        assert_eq!(
            decode_header(&[0xc7, 0xc0]).unwrap().class,
            EncodingClass::Long
        );
        assert_eq!(
            decode_header(&[0xcb, 0xf0]).unwrap().class,
            EncodingClass::ExtraLong
        );
    }

    #[test]
    fn extracts_short_payload_in_stream_order() {
        let header = decode_header(&[0xaa, 0x55]).unwrap();
        assert_eq!(opcode_payload(header, &[0xaa, 0x55]), Some(0x2a55));
    }
}
