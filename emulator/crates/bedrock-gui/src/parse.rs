pub(crate) fn parse_u64(raw: &str) -> Result<u64, String> {
    let compact: String = raw.trim().chars().filter(|ch| *ch != '_').collect();
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

pub(crate) fn parse_usize(raw: &str) -> Result<usize, String> {
    usize::try_from(parse_u64(raw)?).map_err(|_| "value does not fit in usize".to_owned())
}

#[cfg(test)]
mod tests {
    use super::{parse_u64, parse_usize};

    #[test]
    fn parses_decimal_hex_and_underscores() {
        assert_eq!(parse_u64("4096").unwrap(), 4096);
        assert_eq!(parse_u64("0x1_000").unwrap(), 0x1000);
        assert_eq!(parse_usize("0X20").unwrap(), 0x20);
    }

    #[test]
    fn rejects_empty_values() {
        assert!(parse_u64("").is_err());
        assert!(parse_u64("0x").is_err());
    }
}
