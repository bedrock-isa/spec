#include "basic.h"

static volatile double g_fp_sink;
static volatile u64 g_fp_bits_sink;

static u32 fold_fp_byte(u32 checksum, u32 byte, u32 index) {
  checksum = (checksum * 33u) ^ byte ^ (index * 17u);
  return checksum & 0xffu;
}

double basic_fp_series(double x, double y, u32 rounds) {
  for (u32 i = 0; i < rounds; i++) {
    double numerator = (x * y) + 0.75;
    double denominator = y + 0.5;
    double drift = y * 0.03125;
    x = (numerator / denominator) - drift;
    y = y + 0.125;
  }
  g_fp_sink = x;
  return g_fp_sink;
}

u64 basic_fp_bits(double value) {
  union {
    double d;
    u64 u;
  } bits;
  bits.d = value;
  g_fp_bits_sink = bits.u;
  return g_fp_bits_sink;
}

u32 basic_fp_checksum(double value) {
  u64 bits = basic_fp_bits(value);
  const u8 *bytes = (const u8 *)&bits;
  u32 checksum = 0x9du;
  checksum = fold_fp_byte(checksum, bytes[0], 0u);
  checksum = fold_fp_byte(checksum, bytes[1], 1u);
  checksum = fold_fp_byte(checksum, bytes[2], 2u);
  checksum = fold_fp_byte(checksum, bytes[3], 3u);
  checksum = fold_fp_byte(checksum, bytes[4], 4u);
  checksum = fold_fp_byte(checksum, bytes[5], 5u);
  checksum = fold_fp_byte(checksum, bytes[6], 6u);
  checksum = fold_fp_byte(checksum, bytes[7], 7u);
  return checksum;
}
