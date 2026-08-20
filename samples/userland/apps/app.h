#ifndef BEDROCK_USERLAND_APPS_H
#define BEDROCK_USERLAND_APPS_H

typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned char u8;

#include "../../common/bedrock_syscalls.h"

#define APP_REQUEST_COUNT 16u

u32 app_main(void) __attribute__((noinline));
u32 br_syscall(u64 code);
void br_exit(u32 code);
void trigger_privileged_read(void);
u32 app_segment_read_u8(u64 segment, u64 offset);
void app_segment_write_u8(u64 segment, u64 offset, u32 value);
u64 app_segment_image_round_trip(u64 segment);

void app_put_char(u8 ch);
void app_puts(const char *text);
void app_put_hex8(u32 value);
void app_payload(u32 value);
void app_yield(u32 ticket);
void app_user_sum(u32 value);
u32 app_user_result(u32 slot, u32 value);
u32 app_rotl8(u32 value, u32 amount);

#endif
