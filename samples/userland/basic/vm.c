#include "basic.h"

static volatile u32 g_vm_result;
static volatile u64 g_vm_fp_bits;

static u32 clamp_reg(u32 index) { return index & 7u; }

static double load_fvar(u32 index, double f0, double f1, double f2, double f3) {
  index &= 3u;
  if (index == 0u) {
    return f0;
  }
  if (index == 1u) {
    return f1;
  }
  if (index == 2u) {
    return f2;
  }
  return f3;
}

static void store_fvar(u32 index, double value, double *f0, double *f1,
                       double *f2, double *f3) {
  index &= 3u;
  if (index == 0u) {
    *f0 = value;
    return;
  }
  if (index == 1u) {
    *f1 = value;
    return;
  }
  if (index == 2u) {
    *f2 = value;
    return;
  }
  *f3 = value;
}

static u32 rotl8(u32 value, u32 amount) {
  value &= 0xffu;
  amount &= 7u;
  switch (amount) {
  case 0u:
    return value;
  case 1u:
    return ((value << 1u) | (value >> 7u)) & 0xffu;
  case 2u:
    return ((value << 2u) | (value >> 6u)) & 0xffu;
  case 3u:
    return ((value << 3u) | (value >> 5u)) & 0xffu;
  case 4u:
    return ((value << 4u) | (value >> 4u)) & 0xffu;
  case 5u:
    return ((value << 5u) | (value >> 3u)) & 0xffu;
  case 6u:
    return ((value << 6u) | (value >> 2u)) & 0xffu;
  default:
    return ((value << 7u) | (value >> 1u)) & 0xffu;
  }
}

static u32 finish_result(u32 integer_value, double fp_value) {
  u32 fp_checksum = basic_fp_checksum(fp_value);
  g_vm_fp_bits = basic_fp_bits(fp_value);
  g_vm_result = rotl8(integer_value ^ fp_checksum ^ 0x41u, 3);
  return g_vm_result;
}

u32 basic_vm_run(void) {
  u32 vars[8] = {0};
  double f0 = 0.0;
  double f1 = 0.0;
  double f2 = 0.0;
  double f3 = 0.0;
  u32 last_integer = 0;
  double last_float = 0.0;

  for (u32 pc = 0; pc < g_basic_program_len; pc++) {
    const struct BasicInstruction *ins = &g_basic_program[pc];
    u32 dst = clamp_reg(ins->dst);
    u32 src = clamp_reg(ins->src);
    u32 fdst = ins->dst & 3u;
    u32 fsrc = ins->src & 3u;
    double fdst_value = load_fvar(fdst, f0, f1, f2, f3);
    double fsrc_value = load_fvar(fsrc, f0, f1, f2, f3);

    if (ins->opcode == BASIC_OP_END) {
      break;
    }

    switch (ins->opcode) {
    case BASIC_OP_SET:
      vars[dst] = ins->imm;
      break;
    case BASIC_OP_ADD:
      vars[dst] = vars[dst] + vars[src] + ins->imm;
      break;
    case BASIC_OP_MUL:
      vars[dst] = vars[dst] * vars[src];
      break;
    case BASIC_OP_XOR:
      vars[dst] = vars[dst] ^ vars[src] ^ ins->imm;
      break;
    case BASIC_OP_FSET:
      store_fvar(fdst, ins->fimm, &f0, &f1, &f2, &f3);
      break;
    case BASIC_OP_FADD:
      store_fvar(fdst, fdst_value + fsrc_value + ins->fimm, &f0, &f1, &f2, &f3);
      break;
    case BASIC_OP_FMUL:
      store_fvar(fdst, fdst_value * fsrc_value, &f0, &f1, &f2, &f3);
      break;
    case BASIC_OP_FDIV:
      store_fvar(fdst, fdst_value / fsrc_value, &f0, &f1, &f2, &f3);
      break;
    case BASIC_OP_FSERIES:
      store_fvar(fdst, basic_fp_series(fdst_value, fsrc_value, ins->rounds),
                 &f0, &f1, &f2, &f3);
      break;
    case BASIC_OP_PRINT:
      last_integer = vars[dst];
      tty_puts("INT ");
      tty_put_u32_dec(last_integer);
      tty_put_char('\n');
      break;
    case BASIC_OP_FPRINT:
      last_float = load_fvar(fdst, f0, f1, f2, f3);
      g_vm_fp_bits = basic_fp_bits(last_float);
      tty_puts("FPBITS ");
      tty_put_u64_dec(g_vm_fp_bits);
      tty_put_char('\n');
      break;
    default:
      tty_puts("BAD OP ");
      tty_put_u32_dec(ins->opcode);
      tty_put_char('\n');
      return 0xeeu;
    }
  }

  return finish_result(last_integer, last_float);
}
