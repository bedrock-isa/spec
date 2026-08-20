# Draft memory-model validation gate

The formal memory-model domain owns the permitted cross-hart ordering and
visibility of architectural memory actions. Handwritten Sail owns the sequence
of memory actions issued by one hart, but does not determine which cross-hart
orders or observations this model permits. The machine-readable
`validation.yaml` file records the minimum proof obligations adopted for the
current draft.

Within this formal domain, one hart corresponds to one architectural logical processor, and a memory action is the
model-internal representation of an architectural memory event or access.

The gate is deliberately marked `pending_formal_proof`. Structural repository
tests verify that none of the required litmus families or semantic obligations
are dropped, but those tests are not a substitute for an axiomatic or
operational proof. The architecture must not be marked frozen until a formal
model discharges every listed obligation. A failed proof requires an ordered
load/store facility or an explicit SC-fence instruction before freeze.

This closure condition is project planning and validation metadata, not a
second owner of memory behavior. Handwritten memory-model prose is downstream
of the formal model and cannot introduce an additional ordering or visibility
outcome. C-language outcomes and compiler lowerings remain separately owned by
the C ABI.
