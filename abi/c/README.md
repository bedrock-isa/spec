# Bedrock C ABI

`calling_convention.yaml` is the singleton Bedrock C calling convention.
Actual collections keep their inventory inside their directory, for example
`types/types.yaml` and `register_classes/register_classes.yaml`. `model/`
loads and resolves the catalog against the ISA and ELF providers; its
call-layout module projects signatures through the calling convention.
`documents/` contains normative prose. The `c-abi` artifact derives
calling-convention tables from the typed catalog.
