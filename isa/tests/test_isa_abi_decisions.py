#!/usr/bin/env python3
"""Cross-source regression checks for the integrated draft decision record."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_CONTRACT_IDS = {
    "FSINA": 0x0001,
    "FCOSA": 0x0002,
    "FTANA": 0x0003,
    "FSINCOSA": 0x0004,
    "FASINA": 0x0011,
    "FACOSA": 0x0012,
    "FATANA": 0x0013,
    "FSINHA": 0x0021,
    "FCOSHA": 0x0022,
    "FTANHA": 0x0023,
    "FATANHA": 0x0024,
    "FETOXA": 0x0031,
    "FETOXM1A": 0x0032,
    "FTWOTOXA": 0x0033,
    "FTENTOXA": 0x0034,
    "FLOGNA": 0x0041,
    "FLOGNP1A": 0x0042,
    "FLOG2A": 0x0043,
    "FLOG10A": 0x0044,
}


class V1DecisionIntegrationTests(unittest.TestCase):
    def test_fptransa_contract_ids_match_tex_and_details(self) -> None:
        instruction_root = (
            ROOT
            / "isa"
            / "defs"
            / "extensions"
            / "fpu"
            / "extensions"
            / "transcendental_approx"
            / "instructions"
        )
        contract_table = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "fragments"
            / "fptransa_accuracy_contracts.tex"
        ).read_text(encoding="utf-8")
        actual = {
            mnemonic: int(contract_id, 16)
            for contract_id, mnemonic in re.findall(
                r"\\texttt\{0x([0-9a-f]{4})\}\s*&\s*"
                r"\\hyperref\[[^]]+\]\{\\texttt\{([A-Z0-9]+)\}\}",
                contract_table,
            )
        }
        for mnemonic, expected_id in EXPECTED_CONTRACT_IDS.items():
            details = (instruction_root / mnemonic / "details.tex").read_text(encoding="utf-8")
            self.assertIn(f"contract is \\texttt{{0x{expected_id:04x}}}", details)

        self.assertEqual(actual, EXPECTED_CONTRACT_IDS)
        self.assertTrue(all(contract_id & 0xF for contract_id in actual.values()))

    def test_cpuid_headers_and_counter_ids_are_not_payload_zero(self) -> None:
        cpuid = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "cpuid_feature_discovery.tex"
        ).read_text(encoding="utf-8")
        self.assertIn("Index zero of every defined leaf is a common discovery header", cpuid)
        self.assertNotIn(r"\texttt{BASE\_LIMITS} &", cpuid)
        self.assertIn(r"\texttt{MAX\_INDEX=0x0044}", cpuid)

        core_header = (ROOT / "isa" / "c" / "include" / "bedrockcoreintrin.h").read_text(
            encoding="utf-8"
        )
        counters = {
            name: int(value)
            for name, value in re.findall(r"__BEDROCK_PMC_([A-Z]+)\s*=\s*(\d+)", core_header)
        }
        self.assertEqual(counters, {"CYCLE": 1, "INSTRET": 2, "PTWALK": 3})

    def test_repeat_payload_and_encinst_v1_exclusion(self) -> None:
        for mnemonic in ("REPcc", "REPG"):
            definition = yaml.safe_load(
                (
                    ROOT / "isa" / "defs" / "instructions" / mnemonic / "instruction.yaml"
                ).read_text(encoding="utf-8")
            )

        allocation = (ROOT / "isa" / "alloc" / "long.yaml").read_text(encoding="utf-8")
        extension_catalog = (ROOT / "isa" / "defs" / "extensions.yaml").read_text(
            encoding="utf-8"
        )
        cpuid = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "cpuid_feature_discovery.tex"
        ).read_text(encoding="utf-8")
        self.assertNotIn("ENCINST", allocation)
        self.assertNotIn("virtualization_acceleration", extension_catalog)
        self.assertIn("VIRTACCEL", cpuid)

        repg_details = (
            ROOT / "isa" / "defs" / "instructions" / "REPG" / "details.tex"
        ).read_text(encoding="utf-8")
        eret_details = (
            ROOT / "isa" / "defs" / "instructions" / "ERET" / "details.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(r"FRAME\_EXT1", repg_details)
        self.assertNotIn(r"EVENT\_AUX", repg_details)
        self.assertIn(r"always-present FRAME\_EXT1", eret_details)
        self.assertNotIn("require an AUXILIARY frame", eret_details)

    def test_memory_model_gate_lists_every_required_family(self) -> None:
        gate = yaml.safe_load(
            (ROOT / "isa" / "memory_model" / "validation.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(gate["status"], "pending_formal_proof")
        self.assertEqual(
            {entry["id"] for entry in gate["litmus_families"]},
            {"MP", "SB", "LB", "IRIW", "RWC", "release-sequence", "sc-fence", "failed-compare-exchange"},
        )

    def test_result_priority_and_slot_leaf_contract_are_normative(self) -> None:
        execution = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "execution_model.tex"
        ).read_text(encoding="utf-8")
        expected_priority = (
            "Instruction fetch and fetch translation.",
            "Instruction framing and acquisition of the complete instruction record.",
            "Opcode recognition.",
            "Availability of every extension required by the decoded operation.",
            "Fixed-field, reserved-field, and effective-address-form legality.",
            "Privilege checks.",
            "Selector, control-image, and other architectural-state validation.",
            "Predicate evaluation for a conditional operation.",
            "Every non-suppressed operand access in architectural access order.",
            "Execution-stage integer and floating-point exceptions.",
        )
        positions = [execution.index(item) for item in expected_priority]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("complete source read precedes access to the destination", execution)
        self.assertIn("false predicate suppresses", execution)

        translation = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "memory_address_translation.tex"
        ).read_text(encoding="utf-8")
        pte = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "fragments"
            / "page_table_entry_reference.tex"
        ).read_text(encoding="utf-8")
        memory_model = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "memory_model.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(r"\mathit{slot\_address}", translation)
        self.assertIn(r"Q [4095]", translation)
        self.assertIn("no byte-alignment rule", translation)
        self.assertIn(r"Instruction fetch and every atomic", translation)
        self.assertIn(r"\texttt{CP=1}", pte)
        self.assertIn(r"\texttt{A=1}", pte)
        self.assertIn(r"\texttt{D=1}", pte)
        self.assertIn("Transactions to the same slot address preserve program", memory_model)
        self.assertIn("completion of all earlier slot transactions", memory_model)

    def test_machine_check_and_bus_error_recovery_fields(self) -> None:
        auxiliary = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "fragments"
            / "event_auxiliary_payloads.tex"
        ).read_text(encoding="utf-8")
        page_fault = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "fragments"
            / "event_error_codes.tex"
        ).read_text(encoding="utf-8")
        interrupt_model = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "interrupt_model.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(r"10 & \texttt{PRECISE}", auxiliary)
        self.assertIn(r"11 & \texttt{RETRY\_SAFE}", auxiliary)
        self.assertIn(r"29..27 & \texttt{ACCESS\_SIZE}", auxiliary)
        self.assertIn(r"30 & \texttt{RETRY\_SAFE}", auxiliary)
        self.assertIn(r"29..27 & \texttt{ACCESS\_SIZE}", page_fault)
        self.assertIn("slot address and not a byte address", auxiliary)
        self.assertIn(r"\texttt{RETRY\_SAFE=1} requires \texttt{PRECISE=1}", auxiliary)
        for combination in (
            "corrected & 0 & 0",
            "recoverable & 0 & 0",
            "recoverable & 1 & 0",
            "recoverable & 1 & 1",
            "fatal & 0 & 0",
            "fatal & 1 & 0",
        ):
            self.assertIn(combination, auxiliary)
        self.assertIn("All other combinations are invalid", auxiliary)
        self.assertIn("Saved PC is the next instruction that would", auxiliary)
        self.assertIn(r"\texttt{BUS\_ERROR} is a synchronous precise fault", interrupt_model)
        self.assertIn("corrected", interrupt_model)
        self.assertIn(r"\texttt{PRECISE} and \texttt{RETRY\_SAFE} clear", interrupt_model)
        self.assertIn("ERET restores any structurally valid frame mechanically", interrupt_model)

    def test_exact_eager_plt_encoding_and_relocations(self) -> None:
        vectors = yaml.safe_load(
            (ROOT / "isa" / "abi" / "plt_golden_vectors.yaml").read_text(encoding="utf-8")
        )["ordinary_plt"]
        self.assertEqual(vectors["entry_size"], 32)
        self.assertEqual(vectors["alignment"], 16)
        self.assertEqual(vectors["instruction"]["opcode_bytes"], [0xE7, 0xC9, 0x80, 0x67])
        self.assertEqual(vectors["relocation"]["addend"], 4)
        self.assertEqual(vectors["padding"], {"offset": 12, "length": 20, "byte": 0x01})
        self.assertEqual(vectors["got_slot"]["alignment"], 8)

        for vector in vectors["relocation_vectors"]:
            result = vector["got_slot_address"] + vector["addend"] - vector["place"]
            expected = vector.get("result", vector.get("result_signed"))
            self.assertEqual(result, expected)
            encoded = list((result & ((1 << 64) - 1)).to_bytes(8, "little"))
            self.assertEqual(encoded, vector["encoded_little_endian"])

        allocation = yaml.safe_load((ROOT / "isa" / "alloc" / "long.yaml").read_text(encoding="utf-8"))
        jmp = next(entry for entry in allocation["entries"] if entry["id"] == "long.jmp_x_ea_e")
        jcc = next(entry for entry in allocation["entries"] if entry["id"] == "long.jcc_x_ea_e")
        self.assertEqual(jmp["text"], "JMP.X(z:L/Q) <ea>(e)")
        self.assertEqual(jcc["text"], "Jcc.X(z:L/Q) <ea>(e)")

        payload = "1111001001" + "1" + "00000000" + "1100111"
        encoded_opcode = [
            0b11000000 | (9 << 2) | int(payload[:2], 2),
            int(payload[2:10], 2),
            int(payload[10:18], 2),
            int(payload[18:26], 2),
        ]
        self.assertEqual(encoded_opcode, vectors["instruction"]["opcode_bytes"])

        jcc_definition = yaml.safe_load(
            (
                ROOT / "isa" / "defs" / "instructions" / "Jcc" / "instruction.yaml"
            ).read_text(encoding="utf-8")
        )
        sizes_by_types = {
            tuple(operand["type"] for operand in form["operands"]): form.get("sizes", [])
            for form in jcc_definition["forms"]
        }
        for relative_type in ("imm8s", "imm16s", "imm32s"):
            self.assertEqual(sizes_by_types[("condition", relative_type)], ["W", "L"])
        self.assertEqual(sizes_by_types[("condition", "EA")], ["L", "Q"])
        self.assertIn("zero-extends it to the 64-bit near target", jcc_definition["doc"]["description"])

        ea_model = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "effective_address_modes.tex"
        ).read_text(encoding="utf-8")
        self.assertIn("PC naming byte 0 of the current instruction", ea_model)
        self.assertIn("not the address of the following instruction", ea_model)

    def test_atomic_alignment_applies_only_to_byte_addressed_leaves(self) -> None:
        translation = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "memory_address_translation.tex"
        ).read_text(encoding="utf-8")
        memory_model = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "memory_model.tex"
        ).read_text(encoding="utf-8")
        execution_model = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "execution_model.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(r"\texttt{ATOMIC\_ALIGNMENT} applies only", translation)
        self.assertIn(r"misaligned \texttt{AT=0} atomic operand", memory_model)
        self.assertIn("regardless of the numeric slot address", memory_model)
        self.assertIn(r"an \texttt{AT=1} atomic operand raises \texttt{ADDRESS\_TYPE}", execution_model)


if __name__ == "__main__":
    unittest.main()
