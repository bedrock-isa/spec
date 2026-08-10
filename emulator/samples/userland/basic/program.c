#include "basic.h"

static const u32 DEFAULT_BASIC_LINE_NUMBERS[] = {
    10u, 20u, 30u, 40u, 50u, 60u, 70u, 80u, 90u, 100u, 110u,
};

static const char DEFAULT_BASIC_LINE_TEXT[][BASIC_LINE_TEXT_CAP] = {
    "LET A=7",   "LET B=11",       "LET C=A+B",
    "LET D=C*B", "LET E=D XOR 5A", "LET X=1.25",
    "LET Y=2.5", "FOR I=1 TO 12",  "X=((X*Y)+0.75)/(Y+0.5)",
    "NEXT I",    "PRINT E, XBITS",
};

u32 g_basic_line_numbers[BASIC_MAX_LINES];
char g_basic_line_text[BASIC_MAX_LINES][BASIC_LINE_TEXT_CAP];
u32 g_basic_line_count;
struct BasicInstruction g_basic_program[BASIC_COMPILED_CAP];
u32 g_basic_program_len;

static u8 ascii_upper(u8 ch) {
  if (ch == 'a') {
    return 'A';
  }
  if (ch == 'b') {
    return 'B';
  }
  if (ch == 'c') {
    return 'C';
  }
  if (ch == 'd') {
    return 'D';
  }
  if (ch == 'e') {
    return 'E';
  }
  if (ch == 'f') {
    return 'F';
  }
  if (ch == 'g') {
    return 'G';
  }
  if (ch == 'h') {
    return 'H';
  }
  if (ch == 'i') {
    return 'I';
  }
  if (ch == 'j') {
    return 'J';
  }
  if (ch == 'k') {
    return 'K';
  }
  if (ch == 'l') {
    return 'L';
  }
  if (ch == 'm') {
    return 'M';
  }
  if (ch == 'n') {
    return 'N';
  }
  if (ch == 'o') {
    return 'O';
  }
  if (ch == 'p') {
    return 'P';
  }
  if (ch == 'q') {
    return 'Q';
  }
  if (ch == 'r') {
    return 'R';
  }
  if (ch == 's') {
    return 'S';
  }
  if (ch == 't') {
    return 'T';
  }
  if (ch == 'u') {
    return 'U';
  }
  if (ch == 'v') {
    return 'V';
  }
  if (ch == 'w') {
    return 'W';
  }
  if (ch == 'x') {
    return 'X';
  }
  if (ch == 'y') {
    return 'Y';
  }
  if (ch == 'z') {
    return 'Z';
  }
  return ch;
}

static u32 is_space(u8 ch) { return ch == ' ' || ch == '\t'; }

static const char *skip_spaces(const char *text) {
  while (is_space((u8)*text)) {
    text++;
  }
  return text;
}

static u32 decimal_digit_value(u8 ch, u32 *value) {
  if (ch == '0') {
    *value = 0;
    return 1;
  }
  if (ch == '1') {
    *value = 1;
    return 1;
  }
  if (ch == '2') {
    *value = 2;
    return 1;
  }
  if (ch == '3') {
    *value = 3;
    return 1;
  }
  if (ch == '4') {
    *value = 4;
    return 1;
  }
  if (ch == '5') {
    *value = 5;
    return 1;
  }
  if (ch == '6') {
    *value = 6;
    return 1;
  }
  if (ch == '7') {
    *value = 7;
    return 1;
  }
  if (ch == '8') {
    *value = 8;
    return 1;
  }
  if (ch == '9') {
    *value = 9;
    return 1;
  }
  return 0;
}

static u32 hex_digit_value(u8 ch, u32 *value) {
  ch = ascii_upper(ch);
  if (decimal_digit_value(ch, value)) {
    return 1;
  }
  if (ch == 'A') {
    *value = 10;
    return 1;
  }
  if (ch == 'B') {
    *value = 11;
    return 1;
  }
  if (ch == 'C') {
    *value = 12;
    return 1;
  }
  if (ch == 'D') {
    *value = 13;
    return 1;
  }
  if (ch == 'E') {
    *value = 14;
    return 1;
  }
  if (ch == 'F') {
    *value = 15;
    return 1;
  }
  return 0;
}

static u32 is_digit(u8 ch) {
  u32 value = 0;
  return decimal_digit_value(ch, &value);
}

static u32 is_hex_digit(u8 ch) {
  u32 value = 0;
  return hex_digit_value(ch, &value);
}

static u32 hex_value(u8 ch) {
  u32 value = 0;
  hex_digit_value(ch, &value);
  return value;
}

static u32 text_len(const char *text) {
  u32 len = 0;
  while (text[len] != 0) {
    len++;
  }
  return len;
}

static u32 copy_text(char *dst, const char *src, u32 cap) {
  u32 index = 0;
  if (cap == 0u) {
    return 0;
  }
  while (src[index] != 0 && index + 1u < cap) {
    dst[index] = src[index];
    index++;
  }
  dst[index] = 0;
  return src[index] == 0;
}

static u32 match_keyword(const char **text, const char *keyword) {
  const char *p = skip_spaces(*text);
  u32 index = 0;
  while (keyword[index] != 0) {
    if (ascii_upper((u8)p[index]) != (u8)keyword[index]) {
      return 0;
    }
    index++;
  }
  *text = p + index;
  return 1;
}

static u32 consume_char(const char **text, u8 ch) {
  const char *p = skip_spaces(*text);
  if ((u8)*p != ch) {
    return 0;
  }
  *text = p + 1;
  return 1;
}

static u32 parse_line_number(const char *line, u32 *number, const char **body) {
  u32 index = 0;
  u32 value = 0;
  u32 digit = 0;

  while (is_space((u8)line[index])) {
    index++;
  }
  if (!decimal_digit_value((u8)line[index], &digit)) {
    return 0;
  }
  while (decimal_digit_value((u8)line[index], &digit)) {
    value = value * 10u + digit;
    index++;
  }
  while (is_space((u8)line[index])) {
    index++;
  }
  *number = value;
  *body = &line[index];
  return 1;
}

static u32 parse_uint(const char **text, u32 *value) {
  const char *p = skip_spaces(*text);
  u32 base = 10u;
  u32 saw_digit = 0;
  u32 saw_hex_alpha = 0;
  u32 result = 0;

  if (p[0] == '0' && (p[1] == 'x' || p[1] == 'X')) {
    base = 16u;
    p += 2;
  } else {
    const char *scan = p;
    while (is_hex_digit((u8)*scan)) {
      u8 upper = ascii_upper((u8)*scan);
      if (upper >= 'A' && upper <= 'F') {
        saw_hex_alpha = 1;
      }
      scan++;
    }
    if (saw_hex_alpha) {
      base = 16u;
    }
  }

  while ((base == 16u && is_hex_digit((u8)*p)) ||
         (base == 10u && is_digit((u8)*p))) {
    result = result * base + hex_value((u8)*p);
    saw_digit = 1;
    p++;
  }

  if (!saw_digit) {
    return 0;
  }
  *value = result;
  *text = p;
  return 1;
}

static u32 parse_double_value(const char **text, double *value) {
  const char *p = skip_spaces(*text);
  double result = 0.0;
  double place = 0.1;
  u32 saw_digit = 0;

  while (is_digit((u8)*p)) {
    result = result * 10.0 + (double)(*p - '0');
    saw_digit = 1;
    p++;
  }

  if (*p == '.') {
    p++;
    while (is_digit((u8)*p)) {
      result = result + place * (double)(*p - '0');
      place = place * 0.1;
      saw_digit = 1;
      p++;
    }
  }

  if (!saw_digit) {
    return 0;
  }
  *value = result;
  *text = p;
  return 1;
}

static u32 parse_int_var(const char **text, u8 *reg) {
  const char *p = skip_spaces(*text);
  u8 ch = ascii_upper((u8)*p);
  if (ch < 'A' || ch > 'H') {
    return 0;
  }
  *reg = (u8)(ch - 'A');
  *text = p + 1;
  return 1;
}

static u32 parse_float_var(const char **text, u8 *reg) {
  const char *p = skip_spaces(*text);
  u8 ch = ascii_upper((u8)*p);
  if (ch == 'X') {
    *reg = 0;
  } else if (ch == 'Y') {
    *reg = 1;
  } else if (ch == 'Z') {
    *reg = 2;
  } else if (ch == 'W') {
    *reg = 3;
  } else {
    return 0;
  }
  *text = p + 1;
  return 1;
}

static u32 emit(u8 opcode, u8 dst, u8 src, u8 rounds, u32 imm, double fimm) {
  if (g_basic_program_len >= BASIC_COMPILED_CAP) {
    return 0;
  }
  g_basic_program[g_basic_program_len].opcode = opcode;
  g_basic_program[g_basic_program_len].dst = dst;
  g_basic_program[g_basic_program_len].src = src;
  g_basic_program[g_basic_program_len].rounds = rounds;
  g_basic_program[g_basic_program_len].imm = imm;
  g_basic_program[g_basic_program_len].fimm = fimm;
  g_basic_program_len++;
  return 1;
}

static u32 emit_set_from_var(u8 dst, u8 src) {
  if (dst == src) {
    return 1;
  }
  return emit(BASIC_OP_SET, dst, 0, 0, 0u, 0.0) &&
         emit(BASIC_OP_ADD, dst, src, 0, 0u, 0.0);
}

static u32 compile_let_int(const char *expr, u8 dst) {
  u8 lhs_reg = 0;
  u32 lhs_imm = 0;
  u32 lhs_is_reg = parse_int_var(&expr, &lhs_reg);
  if (lhs_is_reg) {
    if (!emit_set_from_var(dst, lhs_reg)) {
      return 0;
    }
  } else if (parse_uint(&expr, &lhs_imm)) {
    if (!emit(BASIC_OP_SET, dst, 0, 0, lhs_imm, 0.0)) {
      return 0;
    }
  } else {
    return 0;
  }

  expr = skip_spaces(expr);
  if (*expr == 0) {
    return 1;
  }

  if (*expr == '+') {
    u8 rhs_reg = 0;
    u32 rhs_imm = 0;
    expr++;
    if (parse_int_var(&expr, &rhs_reg)) {
      return emit(BASIC_OP_ADD, dst, rhs_reg, 0, 0u, 0.0);
    }
    if (parse_uint(&expr, &rhs_imm)) {
      return emit(BASIC_OP_SET, 7, 0, 0, 0u, 0.0) &&
             emit(BASIC_OP_ADD, dst, 7, 0, rhs_imm, 0.0);
    }
    return 0;
  }

  if (*expr == '*') {
    u8 rhs_reg = 0;
    expr++;
    if (!parse_int_var(&expr, &rhs_reg)) {
      return 0;
    }
    return emit(BASIC_OP_MUL, dst, rhs_reg, 0, 0u, 0.0);
  }

  if (match_keyword(&expr, "XOR")) {
    u8 rhs_reg = 0;
    u32 rhs_imm = 0;
    if (parse_int_var(&expr, &rhs_reg)) {
      return emit(BASIC_OP_XOR, dst, rhs_reg, 0, 0u, 0.0);
    }
    if (parse_uint(&expr, &rhs_imm)) {
      return emit(BASIC_OP_SET, 7, 0, 0, 0u, 0.0) &&
             emit(BASIC_OP_XOR, dst, 7, 0, rhs_imm, 0.0);
    }
  }

  return 0;
}

static u32 compile_let(const char *text) {
  u8 dst = 0;
  const char *p = text;
  if (parse_float_var(&p, &dst)) {
    double value = 0.0;
    if (!consume_char(&p, '=') || !parse_double_value(&p, &value)) {
      return 0;
    }
    return emit(BASIC_OP_FSET, dst, 0, 0, 0u, value);
  }

  p = text;
  if (!parse_int_var(&p, &dst) || !consume_char(&p, '=')) {
    return 0;
  }
  return compile_let_int(p, dst);
}

static u32 compile_line(const char *text, u32 *pending_rounds) {
  const char *p = skip_spaces(text);

  if (match_keyword(&p, "LET")) {
    return compile_let(p);
  }

  p = skip_spaces(text);
  if (match_keyword(&p, "FOR")) {
    u32 start = 0;
    u32 end = 0;
    p = skip_spaces(p);
    if (ascii_upper((u8)*p) < 'A' || ascii_upper((u8)*p) > 'Z') {
      return 0;
    }
    p++;
    if (!consume_char(&p, '=') || !parse_uint(&p, &start) ||
        !match_keyword(&p, "TO") || !parse_uint(&p, &end)) {
      return 0;
    }
    *pending_rounds = end >= start ? (end - start + 1u) : 0u;
    if (*pending_rounds > 255u) {
      *pending_rounds = 255u;
    }
    return 1;
  }

  p = skip_spaces(text);
  if (match_keyword(&p, "NEXT")) {
    if (*pending_rounds == 0u) {
      return 1;
    }
    u32 rounds = *pending_rounds;
    *pending_rounds = 0;
    return emit(BASIC_OP_FSERIES, 0, 1, (u8)rounds, 0u, 0.0);
  }

  p = skip_spaces(text);
  if (match_keyword(&p, "X=((X*Y)+0.75)/(Y+0.5)")) {
    return emit(BASIC_OP_FMUL, 0, 1, 0, 0u, 0.0) &&
           emit(BASIC_OP_FADD, 0, 0, 0, 0u, 0.75) &&
           emit(BASIC_OP_FDIV, 0, 1, 0, 0u, 0.0);
  }

  p = skip_spaces(text);
  if (match_keyword(&p, "PRINT")) {
    u8 reg = 0;
    if (match_keyword(&p, "XBITS")) {
      return emit(BASIC_OP_FPRINT, 0, 0, 0, 0u, 0.0);
    }
    if (!parse_int_var(&p, &reg)) {
      return 0;
    }
    if (!emit(BASIC_OP_PRINT, reg, 0, 0, 0u, 0.0)) {
      return 0;
    }
    p = skip_spaces(p);
    if (*p == ',') {
      p++;
      if (match_keyword(&p, "XBITS")) {
        return emit(BASIC_OP_FPRINT, 0, 0, 0, 0u, 0.0);
      }
    }
    return 1;
  }

  p = skip_spaces(text);
  if (match_keyword(&p, "END")) {
    return emit(BASIC_OP_END, 0, 0, 0, 0u, 0.0);
  }

  return 0;
}

void basic_program_reset(void) {
  g_basic_line_count = sizeof(DEFAULT_BASIC_LINE_NUMBERS) /
                       sizeof(DEFAULT_BASIC_LINE_NUMBERS[0]);
  for (u32 i = 0; i < g_basic_line_count; i++) {
    g_basic_line_numbers[i] = DEFAULT_BASIC_LINE_NUMBERS[i];
    copy_text(g_basic_line_text[i], DEFAULT_BASIC_LINE_TEXT[i],
              BASIC_LINE_TEXT_CAP);
  }
}

void basic_program_list(void) {
  for (u32 index = 0; index < g_basic_line_count; index++) {
    tty_put_u32_dec(g_basic_line_numbers[index]);
    tty_put_char(' ');
    tty_puts(g_basic_line_text[index]);
    tty_put_char('\n');
  }
}

u32 basic_program_edit_line(const char *line) {
  u32 number = 0;
  const char *body = 0;
  u32 index = 0;

  if (!parse_line_number(line, &number, &body)) {
    return BASIC_EDIT_NOT_LINE;
  }
  if (number == 0u || text_len(body) >= BASIC_LINE_TEXT_CAP) {
    return BASIC_EDIT_ERROR;
  }

  while (index < g_basic_line_count && g_basic_line_numbers[index] < number) {
    index++;
  }

  if (*body == 0) {
    if (index < g_basic_line_count && g_basic_line_numbers[index] == number) {
      for (u32 move = index; move + 1u < g_basic_line_count; move++) {
        g_basic_line_numbers[move] = g_basic_line_numbers[move + 1u];
        copy_text(g_basic_line_text[move], g_basic_line_text[move + 1u],
                  BASIC_LINE_TEXT_CAP);
      }
      g_basic_line_count--;
    }
    return BASIC_EDIT_OK;
  }

  if (index < g_basic_line_count && g_basic_line_numbers[index] == number) {
    return copy_text(g_basic_line_text[index], body, BASIC_LINE_TEXT_CAP)
               ? BASIC_EDIT_OK
               : BASIC_EDIT_ERROR;
  }

  if (g_basic_line_count >= BASIC_MAX_LINES) {
    return BASIC_EDIT_ERROR;
  }

  for (u32 move = g_basic_line_count; move > index; move--) {
    g_basic_line_numbers[move] = g_basic_line_numbers[move - 1u];
    copy_text(g_basic_line_text[move], g_basic_line_text[move - 1u],
              BASIC_LINE_TEXT_CAP);
  }
  g_basic_line_numbers[index] = number;
  if (!copy_text(g_basic_line_text[index], body, BASIC_LINE_TEXT_CAP)) {
    return BASIC_EDIT_ERROR;
  }
  g_basic_line_count++;
  return BASIC_EDIT_OK;
}

u32 basic_program_compile(void) {
  u32 pending_rounds = 0;
  g_basic_program_len = 0;

  for (u32 index = 0; index < g_basic_line_count; index++) {
    if (!compile_line(g_basic_line_text[index], &pending_rounds)) {
      tty_puts("ERR ");
      tty_put_u32_dec(g_basic_line_numbers[index]);
      tty_put_char('\n');
      g_basic_program_len = 0;
      return 0;
    }
  }

  if (!emit(BASIC_OP_END, 0, 0, 0, 0u, 0.0)) {
    return 0;
  }
  return 1;
}
