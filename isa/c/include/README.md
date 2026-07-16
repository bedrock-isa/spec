# Bedrock target intrinsic headers

These headers are the compiler-facing code interface paired with
`../bedrock-target-intrinsics.tex`. The TeX document owns the semantic contract; these
headers own the wrapper declarations and umbrella include topology.

`bedrockintrin.h` is the public umbrella for far-pointer, core, memory,
integer, and floating-point target interfaces. It deliberately does not include
privileged or system-management interfaces.

`bedrocksystemintrin.h` is the system umbrella for system-register, cache, MMU,
and processor-state interfaces. Every family
header uses the collision-resistant `bedrock<family>intrin.h` spelling and may
also be included directly.

The headers specify the compiler-facing interface. Every function-like use of
`__builtin_bedrock_*` requires target compiler support; these names are not
external runtime functions. Operations with encoded immediate operands use
macro wrappers so the compiler diagnoses nonconstant or out-of-range arguments
at the source call site.
