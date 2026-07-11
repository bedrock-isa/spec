#ifndef __BEDROCKFARINTRIN_H
#define __BEDROCKFARINTRIN_H

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
