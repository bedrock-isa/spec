// Fixed-point wireframe cube sample for the Bedrock emulator.
typedef unsigned long long u64;
typedef unsigned int u32;
typedef int i32;
typedef unsigned char u8;

#define PAGE_PRESENT (1ULL << 0)
#define PAGE_TABLE (1ULL << 1)
#define PAGE_AM_RW (3ULL << 2)
#define PAGE_AM_RX (4ULL << 2)
#define PAGE_AM_MMIO_RW (7ULL << 2)
#define PAGE_TABLE_R (1ULL << 2)
#define PAGE_TABLE_W (1ULL << 3)
#define PAGE_TABLE_X (1ULL << 4)
#define PAGE_USER (1ULL << 5)

#define L4 ((volatile u64 *)0x0000000000008000ULL)
#define L3 ((volatile u64 *)0x0000000000009000ULL)
#define L2 ((volatile u64 *)0x000000000000a000ULL)
#define L1 ((volatile u64 *)0x000000000000b000ULL)

#define HI_BASE 0x00007fff00000000ULL
#define FB ((volatile u8 *)(HI_BASE + 0x0000000000f00000ULL))

#define WIDTH 320
#define HEIGHT 200
#define CENTER_X 160
#define CENTER_Y 100

static const i32 SIN_Q8[32] = {
    0,    50,   98,   142,  181,  213,  236,  251,
    256,  251,  236,  213,  181,  142,  98,   50,
    0,    -50,  -98,  -142, -181, -213, -236, -251,
    -256, -251, -236, -213, -181, -142, -98,  -50,
};

static const i32 RECIP_Q8[32] = {
    320, 320, 320, 320, 320, 320, 300, 280,
    256, 228, 205, 186, 171, 157, 146, 136,
    128, 120, 114, 108, 102, 98,  93,  89,
    85,  82,  79,  76,  73,  71,  68,  66,
};

static const i32 VERTS[8][3] = {
    {-64, -64, -64}, {64, -64, -64}, {64, 64, -64}, {-64, 64, -64},
    {-64, -64, 64},  {64, -64, 64},  {64, 64, 64},  {-64, 64, 64},
};

static const u8 EDGES[12][2] = {
    {0, 1}, {1, 2}, {2, 3}, {3, 0}, {4, 5}, {5, 6},
    {6, 7}, {7, 4}, {0, 4}, {1, 5}, {2, 6}, {3, 7},
};

static const u8 EDGE_COLOR[12] = {
    0xe0, 0xe0, 0xe0, 0xe0, 0x1c, 0x1c,
    0x1c, 0x1c, 0xff, 0xdb, 0xb7, 0x93,
};

static i32 screen_x[8] __attribute__((aligned(4096)));
static i32 screen_y[8];
static volatile u32 delay_sink;

static void map4k(u64 va, u64 pa, u64 flags) {
  u64 l4i = (va >> 39) & 511ULL;
  u64 l3i = (va >> 30) & 511ULL;
  u64 l2i = (va >> 21) & 511ULL;
  u64 l1i = (va >> 12) & 511ULL;

  u64 table = PAGE_PRESENT | PAGE_TABLE | PAGE_TABLE_R | PAGE_TABLE_W |
              PAGE_TABLE_X | PAGE_USER;
  L4[l4i] = 0x9000ULL | table;
  L3[l3i] = 0xa000ULL | table;
  L2[l2i] = 0xb000ULL | table;
  L1[l1i] = (pa & ~0xfffULL) | flags;
}

static void enable_paging(void) {
  u64 mutable_page = ((u64)screen_x) & ~0xfffULL;
  for (u32 page = 1; page < 256; page++) {
    u64 addr = (u64)page * 4096ULL;
    u64 am = (addr == mutable_page || (page >= 8 && page <= 11) || page >= 240)
                 ? PAGE_AM_RW
                 : PAGE_AM_RX;
    map4k(addr, addr, PAGE_PRESENT | am);
  }

  for (u32 page = 0; page < 16; page++) {
    map4k(HI_BASE + 0x00f00000ULL + page * 4096ULL,
          0x00f00000ULL + page * 4096ULL,
          PAGE_PRESENT | PAGE_AM_MMIO_RW);
  }

  __asm__ volatile(
      "MOV.Q 32769, R0\n"
      "SWPT R0"
      :
      :
      : "r0", "memory");
}

static i32 abs_i32(i32 value) {
  return value < 0 ? -value : value;
}

static void put_pixel(i32 x, i32 y, u8 color) {
  if ((u32)x < WIDTH && (u32)y < HEIGHT) {
    FB[(u32)y * WIDTH + (u32)x] = color;
  }
}

static void draw_line(i32 x0, i32 y0, i32 x1, i32 y1, u8 color) {
  i32 dx = abs_i32(x1 - x0);
  i32 sx = x0 < x1 ? 1 : -1;
  i32 dy = -abs_i32(y1 - y0);
  i32 sy = y0 < y1 ? 1 : -1;
  i32 err = dx + dy;

  for (;;) {
    put_pixel(x0, y0, color);
    if (x0 == x1 && y0 == y1) {
      break;
    }

    i32 twice = err + err;
    if (twice >= dy) {
      err += dy;
      x0 += sx;
    }
    if (twice <= dx) {
      err += dx;
      y0 += sy;
    }
  }
}

static void project_cube(u32 angle) {
  i32 sy = SIN_Q8[angle & 31];
  i32 cy = SIN_Q8[(angle + 8) & 31];
  i32 sx = SIN_Q8[(angle + 5) & 31];
  i32 cx = SIN_Q8[(angle + 13) & 31];

  for (u32 i = 0; i < 8; i++) {
    i32 x = VERTS[i][0];
    i32 y = VERTS[i][1];
    i32 z = VERTS[i][2];

    i32 xr = (x * cy + z * sy) >> 8;
    i32 zr = (-x * sy + z * cy) >> 8;
    i32 yr = (y * cx - zr * sx) >> 8;
    i32 zd = ((y * sx + zr * cx) >> 8) + 192;

    i32 depth = zd >> 4;
    if (depth < 0) {
      depth = 0;
    }
    if (depth > 31) {
      depth = 31;
    }

    i32 scale = RECIP_Q8[depth];
    screen_x[i] = CENTER_X + ((xr * scale) >> 8);
    screen_y[i] = CENTER_Y + ((yr * scale) >> 8);
  }
}

static void render_cube(u32 angle, u8 erase) {
  project_cube(angle);
  for (u32 i = 0; i < 12; i++) {
    u32 a = EDGES[i][0];
    u32 b = EDGES[i][1];
    u8 color = erase ? 0x00 : EDGE_COLOR[i];
    draw_line(screen_x[a], screen_y[a], screen_x[b], screen_y[b], color);
  }
}

static void delay(void) {
  for (u32 i = 0; i < 6000; i++) {
    delay_sink += i;
  }
}

void _start(void) {
  enable_paging();

  u32 angle = 0;
  render_cube(angle, 0);
  for (;;) {
    delay();
    render_cube(angle, 1);
    angle = (angle + 1) & 31;
    render_cube(angle, 0);
  }
}
