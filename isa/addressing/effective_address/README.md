# Effective addresses

`definition.yaml` owns the shared effective-address grammar and the compact EA,
FEA, and VEA profile overrides. `decode/` selects the profile named by each
instruction operand, `evaluation/` evaluates decoded addresses and
address-producing instructions, and `manual/` contains the downstream
explanatory TeX sources and generated-fragment inputs.
