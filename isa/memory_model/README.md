# Draft memory-model validation gate

The normative target model is defined by the generated ISA reference's Memory
Model section and by the C ABI's atomic-lowering section. The machine-readable
`validation.yaml` file records the minimum proof obligations adopted for the
current draft.

The gate is deliberately marked `pending_formal_proof`. Structural repository
tests verify that none of the required litmus families or semantic obligations
are dropped, but those tests are not a substitute for an axiomatic or
operational proof. The architecture must not be marked frozen until a formal
model discharges every listed obligation. A failed proof requires an ordered
load/store facility or an explicit SC-fence instruction before freeze.

This closure condition is project planning and validation metadata, not
normative ISA prose. The ISA reference defines only the hardware ordering
target that the model must implement; C-language outcomes and compiler
lowerings remain owned by the C ABI.
