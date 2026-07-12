#ifndef __BEDROCKFARINTRIN_H
#define __BEDROCKFARINTRIN_H

#include <stdint.h>

/* The distinct names document data- and function-pointer use; both aliases
   have the same unsigned 128-bit C type. */
typedef unsigned __int128 __bedrock_far_uintptr_t;
typedef unsigned __int128 __bedrock_far_func_uintptr_t;

#define __BEDROCK_SEGMENT_IMAGE(base_page, exponent, mantissa, bounds_only) \
  ((((uint64_t)(base_page)) << 12) |                                      \
   (((uint64_t)(exponent) & 0x1f) << 7) |                                 \
   (((uint64_t)(mantissa) & 0x3f) << 1) |                                 \
   ((bounds_only) ? UINT64_C(1) : UINT64_C(0)))

#define __BEDROCK_SEGMENT_IMAGE_FOR_BASE(base, exponent, mantissa,           \
                                         bounds_only)                       \
  __BEDROCK_SEGMENT_IMAGE((uint64_t)(base) >> 12, exponent, mantissa,       \
                          bounds_only)

#define __BEDROCK_SEGMENT_DISABLED UINT64_C(0)

#define __BEDROCK_FAR_PTR_INIT(pointer_type, address, segment_image) \
  __builtin_bedrock_far_ptr_init(pointer_type, address, segment_image)
#define __BEDROCK_FAR_FLAT_PTR_INIT(pointer_type, address) \
  __builtin_bedrock_far_flat_ptr_init(pointer_type, address)
#define __BEDROCK_FAR_NULL(pointer_type) \
  __builtin_bedrock_far_null(pointer_type)
#define __BEDROCK_FAR_PTR_FROM_SEGMENT(pointer_type, offset, segment_image) \
  __builtin_bedrock_far_ptr_from_segment(pointer_type, offset, segment_image)

#define __bedrock_far_address(pointer) \
  __builtin_bedrock_far_address(pointer)
#define __bedrock_far_same_encoding(left, right) \
  __builtin_bedrock_far_same_encoding(left, right)

#endif
