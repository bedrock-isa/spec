function concatenated_pair(high : bits(64), low : bits(64), width : int) -> bits(128) =
    if width == 1 then {
        sail_zero_extend(high[7 .. 0] @ low[7 .. 0], 128)
    } else {
        if width == 2 then {
            sail_zero_extend(high[15 .. 0] @ low[15 .. 0], 128)
        } else {
            if width == 4 then {
                sail_zero_extend(high[31 .. 0] @ low[31 .. 0], 128)
            } else {
                high @ low
            }
        }
    }

// Integer data/control behavior is assembled instruction-locally from typed uops.
