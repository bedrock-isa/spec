#!/usr/bin/env python3
"""Helpers for the architectural FPTRANSA accuracy-discovery contract."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import SupportsFloat


FPTRANSA_CPUID_CLASS = 0x00000001
FPTRANSA_ACCURACY_LEAF = 0x0001
FPTRANSA_CONTRACT_REVISION = 1
FPTRANSA_MAX_ULP_Q8_8 = 0x0400
FPTRANSA_MAX_ASSIGNED_CONTRACT_ID = 0x0044

FPTRANSA_CONTRACT_IDS = {
    "FSINA": 0x0001,
    "FCOSA": 0x0002,
    "FTANA": 0x0003,
    "FSINCOSA": 0x0004,
    "FASINA": 0x0011,
    "FACOSA": 0x0012,
    "FATANA": 0x0013,
    "FSINHA": 0x0021,
    "FCOSHA": 0x0022,
    "FTANHA": 0x0023,
    "FATANHA": 0x0024,
    "FETOXA": 0x0031,
    "FETOXM1A": 0x0032,
    "FTWOTOXA": 0x0033,
    "FTENTOXA": 0x0034,
    "FLOGNA": 0x0041,
    "FLOGNP1A": 0x0042,
    "FLOG2A": 0x0043,
    "FLOG10A": 0x0044,
}

FORMAT_PARAMETERS = {
    "S": {"precision_bits": 24, "minimum_normal_exponent": -126},
    "D": {"precision_bits": 53, "minimum_normal_exponent": -1022},
}


@dataclass(frozen=True)
class AccuracyResult:
    present: bool
    revision: int
    s_max_ulp_q8_8: int
    d_max_ulp_q8_8: int


def q8_8_ceiling(value: int | float | str | Fraction) -> int:
    """Encode a nonnegative ULP bound without ever understating it."""
    fraction = value if isinstance(value, Fraction) else Fraction(str(value))
    if fraction < 0:
        raise ValueError("ULP bound must be nonnegative")
    scaled = fraction * 256
    encoded = -(-scaled.numerator // scaled.denominator)
    if encoded > 0xFFFF:
        raise ValueError("ULP bound does not fit unsigned Q8.8")
    return encoded


def q8_8_value(encoded: int) -> Fraction:
    if not 0 <= encoded <= 0xFFFF:
        raise ValueError("Q8.8 field must be a 16-bit unsigned integer")
    return Fraction(encoded, 256)


def cpuid_selector(contract_id: int) -> int:
    if not 1 <= contract_id <= 0xFFFF:
        raise ValueError("contract ID must be a nonzero 16-bit unsigned integer")
    return (FPTRANSA_CPUID_CLASS << 32) | (FPTRANSA_ACCURACY_LEAF << 16) | contract_id


def compose_accuracy_result(
    *,
    present: bool,
    s_max_ulp_q8_8: int = 0,
    d_max_ulp_q8_8: int = 0,
    revision: int = FPTRANSA_CONTRACT_REVISION,
) -> int:
    if not present:
        return 0
    for name, value in (("S", s_max_ulp_q8_8), ("D", d_max_ulp_q8_8)):
        if not 1 <= value <= FPTRANSA_MAX_ULP_Q8_8:
            raise ValueError(f"present {name} bound must be in 0x0001..0x0400")
    if not 0 <= revision <= 0xFF:
        raise ValueError("contract revision must be an 8-bit unsigned integer")
    return (1 << 63) | (revision << 32) | (d_max_ulp_q8_8 << 16) | s_max_ulp_q8_8


def parse_accuracy_result(value: int) -> AccuracyResult:
    if not 0 <= value <= 0xFFFFFFFFFFFFFFFF:
        raise ValueError("CPUID result must be a 64-bit unsigned integer")
    return AccuracyResult(
        present=bool((value >> 63) & 1),
        revision=(value >> 32) & 0xFF,
        s_max_ulp_q8_8=value & 0xFFFF,
        d_max_ulp_q8_8=(value >> 16) & 0xFFFF,
    )


def reference_ulp(reference: SupportsFloat, fmt: str) -> float:
    """Return the architectural ULP quantum for a finite reference value."""
    if fmt not in FORMAT_PARAMETERS:
        raise ValueError(f"unknown floating-point format {fmt!r}")
    value = abs(float(reference))
    if not math.isfinite(value):
        raise ValueError("ULP is defined only for finite reference values")
    parameters = FORMAT_PARAMETERS[fmt]
    p = parameters["precision_bits"]
    emin = parameters["minimum_normal_exponent"]
    minimum_subnormal_exponent = emin - p + 1
    if value == 0.0:
        exponent = minimum_subnormal_exponent
    else:
        _fraction, binary_exponent = math.frexp(value)
        exponent = max(binary_exponent - p, minimum_subnormal_exponent)
    return math.ldexp(1.0, exponent)


def ulp_error(approximate: SupportsFloat, reference: SupportsFloat, fmt: str) -> float:
    exact = float(reference)
    return abs(float(approximate) - exact) / reference_ulp(exact, fmt)
