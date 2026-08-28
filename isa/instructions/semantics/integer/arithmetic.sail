function product_high(lhs : bits(64), rhs : bits(64), width : int, lhs_signed : bool, rhs_signed : bool) -> bits(64) = {
    let left = if lhs_signed then {
            signed_width(lhs, width)
        } else {
            unsigned(narrow_bits(lhs, width))
        };
    let right = if rhs_signed then {
            signed_width(rhs, width)
        } else {
            unsigned(narrow_bits(rhs, width))
        };
    let product : bits(128) = get_slice_int(128, left * right, 0);
    if width == 1 then {
        sail_zero_extend(product[15 .. 8], 64)
    } else {
        if width == 2 then {
            sail_zero_extend(product[31 .. 16], 64)
        } else {
            if width == 4 then {
                sail_zero_extend(product[63 .. 32], 64)
            } else {
                product[127 .. 64]
            }
        }
    }
}

// Integer instruction behavior is assembled instruction-locally from typed uops.
