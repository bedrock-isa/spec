#!/usr/bin/env python3
"""Focused owner-level checks for the canonical Decode IR."""

from __future__ import annotations

from dataclasses import replace
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


TOOLS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_ROOT))

import decode_ir  # noqa: E402
import defs_loader  # noqa: E402
import defs_schema  # noqa: E402


class DecodeIrTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ir = decode_ir.load_decode_ir()
        cls.forms = {form.key: form for form in cls.ir.forms}

    def replace_form(self, replacement: decode_ir.FormIR) -> decode_ir.DecodeIR:
        forms = tuple(
            replacement if form.key == replacement.key else form
            for form in self.ir.forms
        )
        return replace(
            self.ir,
            forms=forms,
        )

    def make_bundle(self, root: Path) -> tuple[Path, dict[str, object]]:
        bundle = root / "SAMPLE"
        bundle.mkdir()
        (bundle / "semantics.sail").write_text(
            "function execute_SAMPLE_low() = ()\n", encoding="utf-8"
        )
        (bundle / "description.tex").write_text(
            "Sample operation.\n", encoding="utf-8"
        )
        encodings = {
            "forms": [
                {
                    "id": "short.sample_x",
                    "class": "short",
                    "bits": "00zssss",
                    "syntax": "SAMPLE.{A|B}(z) Rn(s)",
                    "operands": [
                        {"name": "src", "type": "Rn", "access": "read", "field": "s"}
                    ],
                    "fields": {"z": {"type": "size.TEST"}},
                    "constraints": [
                        {"field": "z", "allow": ["0x0..0x1"], "reason": "reserved"}
                    ],
                }
            ]
        }
        operation: dict[str, object] = {
            "operation": "SAMPLE",
            "title": "Sample Operation",
            "summary": "Exercises the operation-bundle contract.",
            "public_instruction": {"mnemonic": "SAMPLE"},
            "execution_route": "integer_alu",
            "privilege": "unprivileged",
            "repeat": {"kind": "not_eligible"},
            "operands": [
                {
                    "id": "src",
                    "role": "source",
                    "access": "read",
                    "value_domain": "integer",
                    "profiles": ["Rn"],
                }
            ],
            "cases": [
                {
                    "id": "low",
                    "applies_to": {
                        "forms": ["short.sample_x"],
                        "selectors": [{"domain": "TEST", "values": ["A"]}],
                        "operand_profiles": [
                            {"operand": "src", "profiles": ["Rn"]}
                        ],
                    },
                    "additional_requirements": [],
                    "predicate": {"kind": "none"},
                    "flags": [],
                    "events": [],
                    "sail_entry": "execute_SAMPLE_low",
                },
                {
                    "id": "high",
                    "applies_to": {
                        "forms": ["short.sample_x"],
                        "selectors": [{"domain": "TEST", "values": ["B"]}],
                        "operand_profiles": [
                            {"operand": "src", "profiles": ["Rn"]}
                        ],
                    },
                    "additional_requirements": ["EXTRA"],
                    "predicate": {"kind": "none"},
                    "flags": [],
                    "events": [],
                    "sail_entry": "execute_SAMPLE_high",
                },
            ],
            "artifacts": {
                "semantics": {"path": "semantics.sail", "kind": "sail"},
                "description": {"path": "description.tex", "kind": "tex"},
                "diagrams": [],
            },
        }
        (bundle / "encodings.yaml").write_text(
            yaml.safe_dump(encodings, sort_keys=False), encoding="utf-8"
        )
        self.write_operation(bundle, operation)
        return bundle, operation

    def write_operation(self, bundle: Path, operation: dict[str, object]) -> None:
        (bundle / "operation.yaml").write_text(
            yaml.safe_dump(operation, sort_keys=False), encoding="utf-8"
        )

    @staticmethod
    def sample_sizes() -> dict[str, object]:
        return {
            "size_kinds": {
                "TEST": {
                    "values": [
                        {"value": 0, "code": "A"},
                        {"value": 1, "code": "B"},
                    ]
                }
            }
        }

    def load_sample_bundle(
        self,
        bundle: Path,
        *,
        operand_types: dict[str, object] | None = None,
        known_diagram_kinds: frozenset[str] = frozenset(),
        known_event_causes: dict[str, frozenset[str]] | None = None,
        known_flag_effect_definitions: dict[
            str, defs_schema.FlagEffectDefinition
        ] | None = None,
    ) -> defs_loader.CanonicalOperation:
        if known_flag_effect_definitions is None:
            known_flag_effect_definitions = defs_loader.load_flag_effect_definitions(
                decode_ir.DEFAULT_DEFS_ROOT
            )
        if known_event_causes is None:
            known_event_causes = {
                "SAMPLE_EVENT": frozenset({"SAMPLE_CAUSE"})
            }
        return defs_loader.load_operation(
            bundle,
            operand_types={"Rn": {}} if operand_types is None else operand_types,
            size_definitions=self.sample_sizes(),
            base_requirements=("BASE",),
            known_cpuid_flags=frozenset({"BASE", "EXTRA"}),
            known_event_ids=frozenset({"SAMPLE_EVENT"}),
            known_event_causes=known_event_causes,
            known_condition_ids=frozenset(
                {"destination_overlap", "event_condition", "shared_name"}
            ),
            known_named_value_ids=frozenset(
                {"predicate_value", "shared_name"}
            ),
            known_diagram_kinds=known_diagram_kinds,
            known_flag_effect_definitions=known_flag_effect_definitions,
        )

    def make_address_transport_bundle(
        self, root: Path
    ) -> tuple[Path, dict[str, object], dict[str, object]]:
        bundle, operation = self.make_bundle(root)
        encodings: dict[str, object] = {
            "forms": [
                {
                    "id": "medium.sample_ea_e",
                    "class": "medium",
                    "bits": "11101000110eeeeeee",
                    "syntax": "SAMPLE <ea>(e)",
                    "operands": [
                        {
                            "name": "src",
                            "type": "EA",
                            "access": "address",
                            "ea_role": "address",
                            "ea_width": "Q",
                            "field": "e",
                        }
                    ],
                },
                {
                    "id": "medium.sample_rn",
                    "class": "medium",
                    "bits": "11101101000110rrrr",
                    "syntax": "SAMPLE Rn(r)",
                    "operands": [
                        {
                            "name": "src",
                            "type": "Rn",
                            "access": "read",
                            "field": "r",
                        }
                    ],
                },
            ]
        }
        operation["operands"] = [
            {
                "id": "src",
                "role": "address",
                "access": "address",
                "value_domain": "integer",
                "profiles": ["EA", "Rn"],
            }
        ]
        operation["cases"] = [
            {
                "id": "all_forms",
                "applies_to": {
                    "forms": ["medium.sample_ea_e", "medium.sample_rn"]
                },
                "additional_requirements": [],
                "predicate": {"kind": "none"},
                "flags": [],
                "events": [],
                "sail_entry": "execute_SAMPLE_low",
            }
        ]
        (bundle / "encodings.yaml").write_text(
            yaml.safe_dump(encodings, sort_keys=False), encoding="utf-8"
        )
        self.write_operation(bundle, operation)
        return bundle, operation, encodings

    def test_operation_coordinator_loads_a_strict_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle, _ = self.make_bundle(Path(directory))
            operation = self.load_sample_bundle(bundle)
            self.assertEqual(operation.id, "SAMPLE")
            self.assertEqual(operation.title, "Sample Operation")
            self.assertEqual(
                operation.summary, "Exercises the operation-bundle contract."
            )
            self.assertEqual(operation.base_requirements, ("BASE",))
            self.assertEqual(operation.forms, ("short.sample_x",))
            self.assertEqual(tuple(case.id for case in operation.cases), ("low", "high"))
            self.assertEqual(operation.cases[0].resolved_requirements, ("BASE",))
            self.assertEqual(
                operation.cases[1].resolved_requirements, ("BASE", "EXTRA")
            )
            self.assertEqual(operation.artifacts.description.kind, "tex")

    def test_named_value_registry_rejects_invalid_structure(self) -> None:
        valid = {
            "values": [
                {
                    "id": "sample_temporary",
                    "kind": "condition_code_image",
                    "reader_term": "temporary sample result",
                }
            ]
        }
        mutations = (
            (
                "unknown key",
                {**valid, "unexpected": True},
                r"unknown fields unexpected",
            ),
            (
                "duplicate id",
                {"values": [valid["values"][0], valid["values"][0]]},
                r"values.id: duplicate value sample_temporary",
            ),
            (
                "invalid kind",
                {
                    "values": [
                        {**valid["values"][0], "kind": "arbitrary_expression"}
                    ]
                },
                r"values\[0\]\.kind: expected one of condition_code_image",
            ),
        )
        for label, raw, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "named_values.yaml"
                with self.assertRaisesRegex(defs_schema.DecodeError, diagnostic):
                    defs_schema.decode_named_value_registry(path, raw)

    def test_operation_title_and_summary_are_required(self) -> None:
        for field in ("title", "summary"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw.pop(field)
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(
                    defs_schema.DecodeError, rf"missing fields.*{field}"
                ):
                    self.load_sample_bundle(bundle)

    def test_operation_identity_path_and_public_mnemonic_are_independent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            relocated = bundle.with_name("bundle-directory")
            bundle.rename(relocated)
            raw = deepcopy(original)
            raw["operation"] = "sample.operation"
            raw["public_instruction"] = {
                "mnemonic": "CANONICAL",
                "aliases": ["SAMPLE"],
            }
            self.write_operation(relocated, raw)
            operation = self.load_sample_bundle(relocated)
            self.assertEqual(operation.id, "sample.operation")
            self.assertEqual(operation.public_instruction.mnemonic, "CANONICAL")
            self.assertEqual(operation.artifacts.bundle_root, str(relocated.resolve()))
            self.assertEqual(
                operation.artifacts.manifest_path,
                str((relocated / "operation.yaml").resolve()),
            )
            serialized_artifacts = decode_ir._json_value(operation.artifacts)
            for artifact_name in ("semantics", "description"):
                artifact_path = (
                    Path(serialized_artifacts["bundle_root"])
                    / serialized_artifacts[artifact_name]["path"]
                )
                self.assertTrue(artifact_path.is_file(), artifact_path)

            raw["public_instruction"] = {"mnemonic": "CANONICAL"}
            self.write_operation(relocated, raw)
            with self.assertRaisesRegex(
                ValueError, r"short.sample_x.*SAMPLE.*public mnemonic or alias"
            ):
                self.load_sample_bundle(relocated)

    def test_public_builder_projects_a_relocated_canonical_bundle(self) -> None:
        inputs = decode_ir.load_decode_inputs()
        located = inputs.store.for_mnemonic("NOP")[0]
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "unrelated-bundle-directory"
            bundle.mkdir()
            (bundle / "encodings.yaml").write_text(
                yaml.safe_dump(
                    defs_loader.load_yaml(located.path), sort_keys=False
                ),
                encoding="utf-8",
            )
            (bundle / "semantics.sail").write_text(
                "function execute_relocated_nop() = ()\n", encoding="utf-8"
            )
            (bundle / "description.tex").write_text(
                "Synthetic relocated no-operation.\n", encoding="utf-8"
            )
            self.write_operation(
                bundle,
                {
                    "operation": "synthetic.relocated.nop",
                    "title": "Relocated No-Operation",
                    "summary": "Exercises a relocated bundle.",
                    "public_instruction": {
                        "mnemonic": "CANONICALNOP",
                        "aliases": ["NOP"],
                    },
                    "execution_route": "integer_alu",
                    "privilege": "unprivileged",
                    "repeat": {"kind": "not_eligible"},
                    "operands": [],
                    "cases": [
                        {
                            "id": "base",
                            "applies_to": {"forms": [located.form.id]},
                            "additional_requirements": [],
                            "predicate": {"kind": "none"},
                            "flags": [
                                {
                                    "bank": "FFLAGS",
                                    "completion": "accrued_causes",
                                    "effects": [
                                        {"flag": "NV", "effect": "preserve"}
                                    ],
                                }
                            ],
                            "events": [],
                            "sail_entry": "execute_relocated_nop",
                        }
                    ],
                    "artifacts": {
                        "semantics": {
                            "path": "semantics.sail",
                            "kind": "sail",
                        },
                        "description": {
                            "path": "description.tex",
                            "kind": "tex",
                        },
                        "diagrams": [],
                    },
                },
            )
            operation_input = defs_loader.load_operation(
                bundle,
                operand_types=inputs.operand_types,
                known_cpuid_flags=frozenset(),
                known_event_ids=frozenset(),
                known_event_causes={},
                known_condition_ids=frozenset(),
                known_named_value_ids=frozenset(),
                known_diagram_kinds=frozenset(),
                known_flag_effect_definitions=defs_loader.load_flag_effect_definitions(
                    decode_ir.DEFAULT_DEFS_ROOT
                ),
            )
            operations = dict(inputs.operations)
            operations[located.mnemonic] = operation_input

            ir = decode_ir.build_decode_ir(
                inputs.store,
                inputs.operand_types,
                inputs.ea_registry,
                operations,
            )

            operation = next(
                item for item in ir.operations if item.id == operation_input.id
            )
            form = next(item for item in ir.forms if item.key == located.form.id)
            self.assertEqual(operation.public_instruction.mnemonic, "CANONICALNOP")
            self.assertEqual(operation.public_instruction.aliases, ("NOP",))
            self.assertEqual(operation.execution_route, "integer_alu")
            self.assertEqual(operation.logical_operand_ids, ())
            self.assertEqual(operation.operands, ())
            flag_bank = operation.cases[0].flags[0]
            self.assertEqual(flag_bank.bank, "FFLAGS")
            self.assertEqual(
                tuple(effect.flag for effect in flag_bank.effects),
                defs_schema.FLAG_BANK_FLAGS["FFLAGS"],
            )
            self.assertTrue(
                all(effect.effect == "preserve" for effect in flag_bank.effects)
            )
            self.assertEqual(
                operation.artifacts.bundle_root, str(bundle.resolve())
            )
            self.assertEqual(
                operation.artifacts.manifest_path,
                str((bundle / "operation.yaml").resolve()),
            )
            self.assertEqual(form.mnemonic, "NOP")
            self.assertEqual(form.control.route, "integer_alu")
            self.assertEqual(form.control.instruction_class, "")
            self.assertEqual(form.control.family, "")
            self.assertEqual(form.control.predicate_mode, "none")
            self.assertEqual(
                form.annotations,
                decode_ir._operation_annotations(operation_input, located.form.id),
            )

    def test_public_instruction_tokens_have_one_global_operation_owner(self) -> None:
        first, second = self.ir.operations[:2]
        collision = replace(
            second,
            public_instruction=replace(
                second.public_instruction,
                aliases=(
                    *second.public_instruction.aliases,
                    first.public_instruction.mnemonic,
                ),
            ),
        )
        collision_ir = replace(
            self.ir,
            operations=tuple(
                collision if operation.id == second.id else operation
                for operation in self.ir.operations
            ),
        )
        with self.assertRaisesRegex(
            ValueError, r"public instruction token.*belongs to both"
        ):
            decode_ir.validate_decode_ir(collision_ir)

        alias = "OWNERTESTALIAS"
        alias_owner = replace(
            first,
            public_instruction=replace(
                first.public_instruction,
                aliases=(*first.public_instruction.aliases, alias),
            ),
        )
        unused_alias_ir = replace(
            self.ir,
            operations=tuple(
                alias_owner if operation.id == first.id else operation
                for operation in self.ir.operations
            ),
        )
        decode_ir.validate_decode_ir(unused_alias_ir)

        alias_form_key = first.forms[0]
        alias_forms = tuple(
            replace(form, mnemonic=alias) if form.key == alias_form_key else form
            for form in self.ir.forms
        )
        alias_ir = replace(
            unused_alias_ir,
            mnemonics=tuple(sorted({form.mnemonic for form in alias_forms})),
            forms=alias_forms,
            limits=decode_ir._derive_limits(alias_forms, self.ir.effective_addresses),
        )
        decode_ir.validate_decode_ir(alias_ir)

        wrong_owner_forms = tuple(
            replace(form, mnemonic=second.public_instruction.mnemonic)
            if form.key == alias_form_key
            else form
            for form in alias_ir.forms
        )
        wrong_owner_ir = replace(
            alias_ir,
            mnemonics=tuple(
                sorted({form.mnemonic for form in wrong_owner_forms})
            ),
            forms=wrong_owner_forms,
            limits=decode_ir._derive_limits(
                wrong_owner_forms, alias_ir.effective_addresses
            ),
        )
        with self.assertRaisesRegex(
            ValueError, r"form public token.*is not owned by operation"
        ):
            decode_ir.validate_decode_ir(wrong_owner_ir)

    def test_operation_cpuid_requirements_are_known_nonredundant_and_resolved(self) -> None:
        for label, requirements, diagnostic in (
            ("unknown", ["UNKNOWN"], r"unknown case CPUID flags UNKNOWN"),
            ("redundant", ["BASE"], r"repeat inherited CPUID flags BASE"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["cases"][0]["additional_requirements"] = requirements
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.load_sample_bundle(bundle)

    def test_cpuid_registry_and_every_form_availability_rule_match_typed_owners(
        self,
    ) -> None:
        registry = defs_loader.load_cpuid_flags(decode_ir.DEFAULT_DEFS_ROOT)
        self.assertEqual(
            tuple(
                (
                    item.id,
                    item.token,
                    item.selector_class,
                    item.leaf,
                    item.index,
                    item.bit,
                )
                for item in self.ir.cpuid_flags
            ),
            tuple(
                (
                    item.id,
                    item.token,
                    item.location.selector_class,
                    item.location.leaf,
                    item.location.index,
                    item.location.bit,
                )
                for item in registry.values()
            ),
        )
        sizes = defs_loader.load_size_definitions(
            decode_ir.DEFAULT_DEFS_ROOT,
            defs_loader.load_extensions(decode_ir.DEFAULT_DEFS_ROOT),
        )
        operations = {
            form_id: operation
            for operation in self.ir.operations
            for form_id in operation.forms
        }
        for form in self.ir.forms:
            operation = operations[form.key]
            cases = tuple(
                case
                for case in operation.cases
                if form.key in case.applies_to.forms
            )
            with self.subTest(form=form.key):
                self.assertEqual(
                    tuple(rule.case_id for rule in form.availability_rules),
                    tuple(case.id for case in cases),
                )
                self.assertEqual(
                    tuple(
                        rule.required_cpuid_flags
                        for rule in form.availability_rules
                    ),
                    tuple(case.resolved_requirements for case in cases),
                )
                for rule, case in zip(form.availability_rules, cases):
                    self.assertEqual(
                        tuple(item.domain for item in rule.selectors),
                        tuple(item.domain for item in case.applies_to.selectors),
                    )
                    for selector, owner in zip(
                        rule.selectors, case.applies_to.selectors
                    ):
                        encoded = {
                            str(item["code"]): (
                                int(item["value"], 0)
                                if isinstance(item["value"], str)
                                else int(item["value"])
                            )
                            for item in sizes["size_kinds"][owner.domain]["values"]
                        }
                        self.assertEqual(
                            selector.encoded_values,
                            tuple(encoded[value] for value in owner.values),
                        )

    def test_operation_logical_operands_and_profiles_are_exact(self) -> None:
        def remove_operand(raw: dict[str, object]) -> None:
            raw["operands"] = []

        def add_unused_profile(raw: dict[str, object]) -> None:
            raw["operands"][0]["profiles"].append("UnusedProfile")

        def change_access(raw: dict[str, object]) -> None:
            raw["operands"][0]["access"] = "write"

        for label, mutate, diagnostic in (
            ("missing operand", remove_operand, r"operand_profiles.*unknown logical operand"),
            ("unused profile", add_unused_profile, r"src.*unreachable profiles UnusedProfile"),
            ("access", change_access, r"src.*access differs"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                mutate(raw)
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.load_sample_bundle(bundle)

    def test_operation_address_access_accepts_only_ea_and_rn_transports(self) -> None:
        operand_types = {"EA": {}, "Rn": {}, "SP": {}}
        with tempfile.TemporaryDirectory() as directory:
            bundle, _, _ = self.make_address_transport_bundle(Path(directory))
            operation = self.load_sample_bundle(
                bundle, operand_types=operand_types
            )
            self.assertEqual(
                operation.forms, ("medium.sample_ea_e", "medium.sample_rn")
            )

        def logical_role(raw_operation, raw_encodings) -> None:
            raw_operation["operands"][0]["role"] = "source"

        def logical_access(raw_operation, raw_encodings) -> None:
            raw_operation["operands"][0]["access"] = "read"

        def logical_profile_set(raw_operation, raw_encodings) -> None:
            raw_operation["operands"][0]["profiles"].append("SP")

        def ea_value_read(raw_operation, raw_encodings) -> None:
            operand = raw_encodings["forms"][0]["operands"][0]
            operand["access"] = "read"
            operand["ea_role"] = "value"

        def ea_missing_role(raw_operation, raw_encodings) -> None:
            del raw_encodings["forms"][0]["operands"][0]["ea_role"]

        def ea_write(raw_operation, raw_encodings) -> None:
            raw_encodings["forms"][0]["operands"][0]["access"] = "write"

        def rn_address(raw_operation, raw_encodings) -> None:
            raw_encodings["forms"][1]["operands"][0]["access"] = "address"

        def rn_write(raw_operation, raw_encodings) -> None:
            raw_encodings["forms"][1]["operands"][0]["access"] = "write"

        def rn_read_write(raw_operation, raw_encodings) -> None:
            raw_encodings["forms"][1]["operands"][0]["access"] = "read_write"

        def outside_profile(raw_operation, raw_encodings) -> None:
            raw_encodings["forms"][1]["operands"][0]["type"] = "SP"

        mutations = (
            ("logical role", logical_role, r"logical role 'source'"),
            (
                "logical access",
                logical_access,
                r"logical role 'address', access 'read'",
            ),
            (
                "logical profile set",
                logical_profile_set,
                r"profiles \('EA', 'Rn', 'SP'\)",
            ),
            ("EA missing role", ea_missing_role, r"require ea_role and ea_width"),
            ("EA write", ea_write, r"address role requires address access"),
            (
                "EA value read",
                ea_value_read,
                r"encoded profile 'EA', access 'read', ea_role 'value'",
            ),
            ("Rn address", rn_address, r"encoded profile 'Rn', access 'address'"),
            ("Rn write", rn_write, r"encoded profile 'Rn', access 'write'"),
            (
                "Rn read-write",
                rn_read_write,
                r"encoded profile 'Rn', access 'read_write'",
            ),
            ("outside profile", outside_profile, r"uses undeclared profile 'SP'"),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, operation, encodings = self.make_address_transport_bundle(
                    Path(directory)
                )
                mutate(operation, encodings)
                self.write_operation(bundle, operation)
                (bundle / "encodings.yaml").write_text(
                    yaml.safe_dump(encodings, sort_keys=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.load_sample_bundle(bundle, operand_types=operand_types)

    def test_operation_route_and_value_domain_use_closed_registries(self) -> None:
        for value_domain in ("vector", "predicate"):
            with self.subTest(pilot_domain=value_domain), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["execution_route"] = "vector"
                raw["operands"][0]["value_domain"] = value_domain
                self.write_operation(bundle, raw)
                self.load_sample_bundle(bundle)

        for label, field, value, diagnostic in (
            (
                "execution route",
                "execution_route",
                "unknown_route",
                r"execution_route.*expected one of",
            ),
            (
                "unknown operand value domain",
                "value_domain",
                "unknown_domain",
                r"operands\[0\]\.value_domain.*expected one of",
            ),
            (
                "address value domain",
                "value_domain",
                "address",
                r"operands\[0\]\.value_domain.*expected one of",
            ),
            (
                "opaque value domain",
                "value_domain",
                "opaque-bits",
                r"operands\[0\]\.value_domain.*expected one of",
            ),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                if field == "execution_route":
                    raw[field] = value
                else:
                    raw["operands"][0][field] = value
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(defs_schema.DecodeError, diagnostic):
                    self.load_sample_bundle(bundle)

    def test_operation_repeat_and_predicate_references_are_typed(self) -> None:
        for observed in (
            {"kind": "computed"},
            {"kind": "result", "operand": "src"},
            {"kind": "source", "operand": "src"},
        ):
            with self.subTest(observed=observed), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["repeat"] = {"kind": "rep_and_repcc", "observed": observed}
                self.write_operation(bundle, raw)
                self.assertEqual(
                    self.load_sample_bundle(bundle).repeat.kind, "rep_and_repcc"
                )

        for label, repeat, diagnostic in (
            (
                "computed payload",
                {
                    "kind": "rep_and_repcc",
                    "observed": {"kind": "computed", "operand": "src"},
                },
                r"computed observation has no operand",
            ),
            (
                "unknown operand",
                {"kind": "rep_and_repcc", "observed": {"kind": "result", "operand": "missing"}},
                r"repeat.observed.operand.*unknown logical operand",
            ),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["repeat"] = repeat
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex((ValueError, defs_schema.DecodeError), diagnostic):
                    self.load_sample_bundle(bundle)

        for observed, diagnostic in (
            ("predicate_value", None),
            ("shared_name", None),
            ("unknown", r"predicates reference unknown named value IDs unknown"),
        ):
            with self.subTest(predicate_observed=observed), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["cases"][0]["predicate"] = {
                    "kind": "test_temporary",
                    "condition_operand": "src",
                    "observed": observed,
                }
                self.write_operation(bundle, raw)
                if diagnostic is None:
                    self.load_sample_bundle(bundle)
                else:
                    with self.assertRaisesRegex(ValueError, diagnostic):
                        self.load_sample_bundle(bundle)
        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            raw = deepcopy(original)
            raw["cases"][0]["predicate"] = {
                "kind": "annul_on_false",
                "condition_operand": "missing",
            }
            self.write_operation(bundle, raw)
            with self.assertRaisesRegex(
                defs_schema.DecodeError, r"predicate.condition_operand.*unknown logical operand"
            ):
                self.load_sample_bundle(bundle)

    def test_operation_flag_event_and_diagram_refs_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            raw = deepcopy(original)
            raw["cases"][0]["flags"] = [
                {
                    "bank": "FFLAGS",
                    "completion": "accrued_causes",
                    "effects": [
                        {"flag": "NV", "effect": "preserve"},
                        {
                            "flag": "OF",
                            "effect": "accrue_source",
                            "reference": "operation_cause",
                        },
                    ],
                }
            ]
            raw["cases"][0]["events"] = [
                {"event": "SAMPLE_EVENT", "condition": "shared_name"}
            ]
            self.write_operation(bundle, raw)
            operation = self.load_sample_bundle(bundle)
            effects = operation.cases[0].flags[0].effects
            self.assertEqual(
                tuple(effect.flag for effect in effects),
                defs_schema.FLAG_BANK_FLAGS["FFLAGS"],
            )
            self.assertEqual(
                tuple(effect.effect for effect in effects),
                ("preserve", "preserve", "accrue_source", "preserve", "preserve"),
            )
            self.assertEqual(effects[2].reference, "operation_cause")
            self.assertTrue(
                all(
                    effect.reference is None
                    for effect in (*effects[:2], *effects[3:])
                )
            )

        invalid_flags = (
            (
                "duplicate flag",
                {
                    "bank": "FFLAGS",
                    "completion": "accrued_causes",
                    "effects": [
                        {"flag": "NV", "effect": "preserve"},
                        {"flag": "NV", "effect": "preserve"},
                    ],
                },
                r"effects.flag.*duplicate value NV",
            ),
            (
                "unknown flag",
                {
                    "bank": "FFLAGS",
                    "completion": "accrued_causes",
                    "effects": [{"flag": "UNKNOWN", "effect": "preserve"}],
                },
                r"flag.*expected one of",
            ),
            (
                "wrong completion",
                {
                    "bank": "FFLAGS",
                    "completion": "complete_image",
                    "effects": [{"flag": "NV", "effect": "preserve"}],
                },
                r"completion.*FFLAGS requires accrued_causes",
            ),
            (
                "condition in accrued bank",
                {
                    "bank": "FFLAGS",
                    "completion": "accrued_causes",
                    "effects": [
                        {
                            "flag": "NV",
                            "effect": "write_condition",
                            "reference": "result_zero",
                        }
                    ],
                },
                r"write_condition is not valid for accrued_causes",
            ),
            (
                "accrual in complete image",
                {
                    "bank": "FLAGS",
                    "completion": "complete_image",
                    "effects": [
                        {
                            "flag": "Z",
                            "effect": "accrue_source",
                            "reference": "operation_cause",
                        }
                    ],
                },
                r"accrue_source is not valid for complete_image",
            ),
            (
                "missing reference",
                {
                    "bank": "FFLAGS",
                    "completion": "accrued_causes",
                    "effects": [
                        {"flag": "NV", "effect": "accrue_source"}
                    ],
                },
                r"accrue_source requires exactly reference",
            ),
            (
                "constant reference",
                {
                    "bank": "FLAGS",
                    "completion": "complete_image",
                    "effects": [
                        {"flag": "Z", "effect": "clear", "reference": "result_zero"}
                    ],
                },
                r"clear requires exactly no reference fields",
            ),
        )
        for label, flag_contract, diagnostic in invalid_flags:
            with self.subTest(flag_contract=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["cases"][0]["flags"] = [flag_contract]
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(defs_schema.DecodeError, diagnostic):
                    self.load_sample_bundle(bundle)

        for reference, definitions, diagnostic in (
            (
                "unknown_definition",
                defs_loader.load_flag_effect_definitions(
                    decode_ir.DEFAULT_DEFS_ROOT
                ),
                r"unknown flag effect definition 'unknown_definition'",
            ),
            (
                "result_zero",
                {
                    **defs_loader.load_flag_effect_definitions(
                        decode_ir.DEFAULT_DEFS_ROOT
                    ),
                    "result_zero": defs_schema.FlagEffectDefinition(
                        "result_zero", "expression", "result == 0"
                    ),
                },
                r"uses 'expression' definition 'result_zero'.*expected 'condition'",
            ),
        ):
            with self.subTest(reference=reference), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["cases"][0]["flags"] = [
                    {
                        "bank": "FLAGS",
                        "completion": "complete_image",
                        "effects": [
                            {
                                "flag": "Z",
                                "effect": "write_condition",
                                "reference": reference,
                            }
                        ],
                    }
                ]
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.load_sample_bundle(
                        bundle,
                        known_flag_effect_definitions=definitions,
                    )

        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            raw = deepcopy(original)
            raw["cases"][0]["events"] = [
                {"event": "UNKNOWN_EVENT", "condition": "event_condition"}
            ]
            self.write_operation(bundle, raw)
            with self.assertRaisesRegex(ValueError, r"unknown event IDs UNKNOWN_EVENT"):
                self.load_sample_bundle(bundle)

        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            raw = deepcopy(original)
            raw["cases"][0]["events"] = [
                {"event": "SAMPLE_EVENT", "condition": "unknown"}
            ]
            self.write_operation(bundle, raw)
            with self.assertRaisesRegex(ValueError, r"unknown semantic condition IDs unknown"):
                self.load_sample_bundle(bundle)

        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            raw = deepcopy(original)
            raw["cases"][0]["events"] = [
                {
                    "event": "SAMPLE_EVENT",
                    "condition": "event_condition",
                    "cause": "SAMPLE_CAUSE",
                }
            ]
            self.write_operation(bundle, raw)
            operation = self.load_sample_bundle(bundle)
            self.assertEqual(operation.cases[0].events[0].cause, "SAMPLE_CAUSE")

        duplicate_event_contracts = (
            (
                "exact duplicate",
                ("SAMPLE_CAUSE", "SAMPLE_CAUSE"),
            ),
            (
                "same pair with different causes",
                ("SAMPLE_CAUSE", "OTHER_CAUSE"),
            ),
        )
        for label, causes in duplicate_event_contracts:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["cases"][0]["events"] = [
                    {
                        "event": "SAMPLE_EVENT",
                        "condition": "event_condition",
                        "cause": cause,
                    }
                    for cause in causes
                ]
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(
                    defs_schema.DecodeError,
                    r"events: duplicate value \('SAMPLE_EVENT', 'event_condition'\)",
                ):
                    self.load_sample_bundle(
                        bundle,
                        known_event_causes={
                            "SAMPLE_EVENT": frozenset(causes),
                        },
                    )

        cause_mutations = (
            (
                "event without cause space",
                {"SAMPLE_EVENT": frozenset()},
                "SAMPLE_CAUSE",
                r"SAMPLE_EVENT has no architected cause space for SAMPLE_CAUSE",
            ),
            (
                "cause owned by another event",
                {
                    "SAMPLE_EVENT": frozenset(),
                    "OTHER_EVENT": frozenset({"SAMPLE_CAUSE"}),
                },
                "SAMPLE_CAUSE",
                r"cause SAMPLE_CAUSE belongs to OTHER_EVENT, not SAMPLE_EVENT",
            ),
            (
                "unknown cause",
                {"SAMPLE_EVENT": frozenset({"KNOWN_CAUSE"})},
                "UNKNOWN_CAUSE",
                r"SAMPLE_EVENT has unknown architectural cause UNKNOWN_CAUSE",
            ),
        )
        for label, cause_spaces, cause, diagnostic in cause_mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                raw["cases"][0]["events"] = [
                    {
                        "event": "SAMPLE_EVENT",
                        "condition": "event_condition",
                        "cause": cause,
                    }
                ]
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.load_sample_bundle(
                        bundle, known_event_causes=cause_spaces
                    )

        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            raw = deepcopy(original)
            raw["cases"][0]["events"] = [
                {
                    "event": "SAMPLE_EVENT",
                    "condition": "destination_overlap",
                }
            ]
            self.write_operation(bundle, raw)
            with self.assertRaisesRegex(
                ValueError,
                r"destination-overlap event requires an illegal_instruction "
                r"destination_overlap relation in forms short.sample_x",
            ):
                self.load_sample_bundle(bundle)

        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            (bundle / "diagrams").mkdir()
            (bundle / "diagrams" / "sample.yaml").write_text("example: sample\n", encoding="utf-8")
            raw = deepcopy(original)
            raw["artifacts"]["diagrams"] = [
                {
                    "id": "sample-view",
                    "path": "diagrams/sample.yaml",
                    "kind": "unregistered",
                    "case": "low",
                    "caption": "Sample view.",
                    "alt_text": "Sample nonvisual view.",
                }
            ]
            self.write_operation(bundle, raw)
            with self.assertRaisesRegex(ValueError, r"unknown diagram kinds unregistered"):
                self.load_sample_bundle(bundle)

        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            (bundle / "diagrams").mkdir()
            (bundle / "diagrams" / "sample.yaml").write_text("kind: sample\n", encoding="utf-8")
            raw = deepcopy(original)
            raw["artifacts"]["diagrams"] = [
                {
                    "id": "sample-view",
                    "path": "diagrams/sample.yaml",
                    "kind": "registered",
                    "case": "missing",
                    "caption": "Sample view.",
                    "alt_text": "Sample nonvisual view.",
                }
            ]
            self.write_operation(bundle, raw)
            with self.assertRaisesRegex(ValueError, r"diagrams reference unknown case IDs missing"):
                self.load_sample_bundle(bundle, known_diagram_kinds=frozenset({"registered"}))

    def test_operation_loader_requires_a_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle, _ = self.make_bundle(Path(directory))
            (bundle / "operation.yaml").unlink()
            with self.assertRaisesRegex(ValueError, r"SAMPLE.*expected operation.yaml"):
                self.load_sample_bundle(bundle)

    def test_operation_coordinator_rejects_invalid_artifacts(self) -> None:
        mutations = (
            (
                "traversal",
                lambda raw: raw["artifacts"].__setitem__(
                    "semantics", {"path": "../outside.sail", "kind": "sail"}
                ),
                r"artifacts.semantics.path.*normalized relative path",
            ),
            (
                "missing",
                lambda raw: raw["artifacts"].__setitem__(
                    "semantics", {"path": "missing.sail", "kind": "sail"}
                ),
                r"operation.yaml.*missing.sail.*does not exist",
            ),
            (
                "wrong kind",
                lambda raw: raw["artifacts"].__setitem__(
                    "semantics", {"path": "description.tex", "kind": "sail"}
                ),
                r"operation.yaml.*description.tex.*wrong file kind",
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                mutate(raw)
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex((ValueError, defs_schema.DecodeError), diagnostic):
                    self.load_sample_bundle(bundle)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle, original = self.make_bundle(root)
            outside = root / "outside.sail"
            outside.write_text("function outside() = ()\n", encoding="utf-8")
            (bundle / "linked.sail").symlink_to(outside)
            raw = deepcopy(original)
            raw["artifacts"]["semantics"] = {
                "path": "linked.sail",
                "kind": "sail",
            }
            self.write_operation(bundle, raw)
            with self.assertRaisesRegex(ValueError, r"operation.yaml.*linked.sail.*outside"):
                self.load_sample_bundle(bundle)

    def test_operation_coordinator_derives_membership_and_validates_case_forms(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle, original = self.make_bundle(Path(directory))
            encodings_path = bundle / "encodings.yaml"
            encodings = yaml.safe_load(encodings_path.read_text(encoding="utf-8"))
            second = deepcopy(encodings["forms"][0])
            second["id"] = "short.sample_second"
            encodings["forms"].append(second)
            encodings_path.write_text(
                yaml.safe_dump(encodings, sort_keys=False), encoding="utf-8"
            )
            raw = deepcopy(original)
            for case in raw["cases"]:
                case["applies_to"]["forms"].append("short.sample_second")
            self.write_operation(bundle, raw)
            self.assertEqual(
                self.load_sample_bundle(bundle).forms,
                ("short.sample_x", "short.sample_second"),
            )

        mutations = (
            (
                "top-level duplicate owner",
                lambda raw: raw.__setitem__("forms", ["short.sample_x"]),
                r"operation.yaml.*unknown fields forms",
            ),
            (
                "duplicate case form",
                lambda raw: raw["cases"][0]["applies_to"]["forms"].append(
                    "short.sample_x"
                ),
                r"cases\[0\]\.applies_to\.forms.*duplicate",
            ),
            (
                "unknown case form",
                lambda raw: raw["cases"][0]["applies_to"].__setitem__(
                    "forms", ["short.sample_extra"]
                ),
                r"operation.yaml.*case 'low'.*applies_to\.forms.*unknown encoding forms.*short.sample_extra",
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                mutate(raw)
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex((ValueError, defs_schema.DecodeError), diagnostic):
                    self.load_sample_bundle(bundle)

        with tempfile.TemporaryDirectory() as directory:
            bundle, _ = self.make_bundle(Path(directory))
            encodings_path = bundle / "encodings.yaml"
            encodings = yaml.safe_load(encodings_path.read_text(encoding="utf-8"))
            second = deepcopy(encodings["forms"][0])
            second["id"] = "short.sample_second"
            encodings["forms"].append(second)
            encodings_path.write_text(
                yaml.safe_dump(encodings, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, r"operation.yaml.*cases leave a gap.*short.sample_second"
            ):
                self.load_sample_bundle(bundle)

    def test_operation_cases_must_be_total_exclusive_and_reachable(self) -> None:
        def overlap(raw: dict[str, object]) -> None:
            raw["cases"][1]["applies_to"]["selectors"][0]["values"] = ["A"]

        def gap(raw: dict[str, object]) -> None:
            raw["cases"] = raw["cases"][:1]

        def unreachable(raw: dict[str, object]) -> None:
            extra = deepcopy(raw["cases"][1])
            extra["id"] = "unreachable"
            extra["applies_to"]["selectors"][0]["values"] = ["C"]
            raw["cases"].append(extra)

        for label, mutate, diagnostic in (
            ("overlap", overlap, r"operation.yaml.*cases overlap.*short.sample_x"),
            ("gap", gap, r"operation.yaml.*cases leave a gap.*short.sample_x"),
            ("unreachable", unreachable, r"operation.yaml.*unreachable values.*C"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                bundle, original = self.make_bundle(Path(directory))
                raw = deepcopy(original)
                mutate(raw)
                self.write_operation(bundle, raw)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.load_sample_bundle(bundle)
    def test_non_contiguous_fields_use_msb_to_lsb_gathers(self) -> None:
        form = self.forms["medium.abs_x_ea"]
        ea_field = next(field for field in form.fields if field.symbol == "e")
        self.assertEqual(ea_field.positions, (6, 5, 4, 3, 2, 1, 0))
        self.assertTrue(all(
            left > right for left, right in zip(ea_field.positions, ea_field.positions[1:])
        ))

    def test_operand_source_variants_come_from_live_forms(self) -> None:
        tags = {
            operand.source.tag
            for form in self.ir.forms
            for operand in form.operands
        }
        self.assertEqual(
            tags,
            {"encoded-field", "fixed", "appended-payload", "effective-address"},
        )
        fixed = self.forms["extrashort.add_q_8_sp"].operands
        self.assertEqual(fixed[0].source, decode_ir.FixedSourceIR(8, ""))
        self.assertEqual(fixed[1].source, decode_ir.FixedSourceIR(None, "SP"))
        appended = self.forms["medium.fmovcr_x_imm16_fn_d"].operands[0].source
        self.assertEqual(appended, decode_ir.AppendedPayloadSourceIR(16, False))
        ea = self.forms["medium.abs_x_ea"].operands[0].source
        self.assertIsInstance(ea, decode_ir.EffectiveAddressSourceIR)

    def test_layout_orders_all_eas_before_appended_payloads(self) -> None:
        two_ea = self.forms["long.cmp_x_ea_s_ea_d"]
        self.assertEqual(
            [(item.tag, item.operand_name) for item in two_ea.layout],
            [("ParseEa", "lhs"), ("ParseEa", "rhs")],
        )
        ea_and_payload = self.forms["medium.add_q_imm64_ea_e"]
        self.assertEqual(
            [(item.tag, item.operand_name) for item in ea_and_payload.layout],
            [("ParseEa", "dst"), ("ReadPayload", "src")],
        )
        self.assertEqual(ea_and_payload.fixed_required_bytes, 11)
        self.assertEqual(ea_and_payload.maximum_required_bytes, 21)

    def test_compact_table_is_complete_and_reserved_values_are_explicit(self) -> None:
        entries = self.ir.effective_addresses.compact_entries
        self.assertEqual(tuple(entry.raw for entry in entries), tuple(range(128)))
        invalid = [entry for entry in entries if not entry.valid]
        self.assertEqual([entry.raw for entry in invalid], list(range(0x69, 0x80)))
        self.assertTrue(all(entry.reserved and entry.invalid_reason for entry in invalid))
        self.assertTrue(all(
            entry.descriptor_bytes in {0, 1, 2}
            and entry.consumed_bytes == entry.descriptor_bytes + entry.payload_width // 8
            for entry in entries
            if entry.valid
        ))

    def test_all_compact_profiles_are_complete_and_preserve_shared_contracts(self) -> None:
        profiles = {
            profile.name: profile
            for profile in self.ir.effective_addresses.profiles
        }
        self.assertEqual(set(profiles), {"ea", "fea", "vea"})
        for name, profile in profiles.items():
            with self.subTest(profile=name):
                self.assertEqual(
                    tuple(entry.raw for entry in profile.compact_entries),
                    tuple(range(128)),
                )

        ea = profiles["ea"].compact_entries
        fea = profiles["fea"].compact_entries
        vea = profiles["vea"].compact_entries
        for raw in range(128):
            if raw not in {0x58, 0x5B, 0x5C, 0x5D, 0x5E}:
                shared = (
                    "valid", "reserved", "form_name", "kind", "payload_width",
                    "payload_signed", "descriptor_family", "descriptor_bytes",
                    "consumed_bytes",
                )
                self.assertEqual(
                    tuple(getattr(fea[raw], field) for field in shared),
                    tuple(getattr(ea[raw], field) for field in shared),
                    raw,
                )
                self.assertEqual(
                    tuple(getattr(vea[raw], field) for field in shared),
                    tuple(getattr(ea[raw], field) for field in shared),
                    raw,
                )
        self.assertTrue(all(not fea[raw].valid for raw in (0x58, 0x5B, 0x5C)))
        self.assertEqual(
            [
                (
                    next(
                        form.payload_name
                        for form in profiles["fea"].compact_forms
                        if form.name == fea[raw].form_name
                    ),
                    fea[raw].payload_width,
                )
                for raw in (0x5D, 0x5E)
            ],
            [("immsf", 32), ("immdf", 64)],
        )
        self.assertTrue(all(
            not vea[raw].valid and vea[raw].reserved
            for raw in (0x58, 0x5B, 0x5C, 0x5D, 0x5E)
        ))
        for profile in profiles.values():
            self.assertEqual(
                [profile.compact_entries[raw].descriptor_family for raw in range(0x5F, 0x69)],
                [entry.descriptor_family for entry in ea[0x5F:0x69]],
            )

    def test_descriptor_families_keep_exact_lengths_and_mask_value_forms(self) -> None:
        families = {
            family.name: family
            for family in self.ir.effective_addresses.descriptor_families
        }
        self.assertEqual(set(families), {"ext1", "ext2"})
        self.assertEqual(families["ext1"].descriptor_bytes, 1)
        self.assertEqual(families["ext2"].descriptor_bytes, 2)
        for name, family in families.items():
            expected_width = family.descriptor_bytes * 8
            with self.subTest(family=name):
                self.assertTrue(family.forms)
                self.assertTrue(all(
                    form.member_of_descriptor_family == name
                    and not form.referenced_descriptor_family
                    for form in family.forms
                ))
                self.assertTrue(all(form.width == expected_width for form in family.forms))
                self.assertTrue(all(form.value & ~form.mask == 0 for form in family.forms))
                self.assertTrue(all(
                    len(form.patterns) == family.descriptor_bytes
                    for form in family.forms
                ))
        compact_escape = next(
            form
            for form in self.ir.effective_addresses.compact_forms
            if form.referenced_descriptor_family == "ext1"
        )
        self.assertEqual(compact_escape.member_of_descriptor_family, "")
        serialized_ea = decode_ir.decode_ir_dict(self.ir)["effective_addresses"]
        serialized_compact = next(
            form
            for form in serialized_ea["compact_forms"]
            if form["name"] == compact_escape.name
        )
        serialized_ext1 = next(
            family for family in serialized_ea["descriptor_families"]
            if family["name"] == "ext1"
        )["forms"][0]
        self.assertEqual(serialized_compact["referenced_descriptor_family"], "ext1")
        self.assertEqual(serialized_compact["member_of_descriptor_family"], "")
        self.assertEqual(serialized_ext1["member_of_descriptor_family"], "ext1")
        self.assertEqual(serialized_ext1["referenced_descriptor_family"], "")
        self.assertNotIn("descriptor_family", serialized_compact)
        self.assertNotIn("descriptor", serialized_compact)

    def test_vector_memory_redesign_owns_exact_patterns_and_payload_lengths(self) -> None:
        def pattern(form: decode_ir.FormIR) -> str:
            by_position = {
                position: field.symbol
                for field in form.fields
                for position in field.positions
            }
            return "".join(
                str((form.opcode_value >> position) & 1)
                if form.opcode_mask & (1 << position)
                else by_position[position]
                for position in range(form.opcode_width - 1, -1, -1)
            )

        gather = [
            "111111110000010000zz0bbbbppppiiiissssvvvvv",
            "111111110000010001000000ppppiiiivvvvvxxxxx",
            "111111110000010001000001ppppiiiivvvvvxxxxx",
            "111111110000010010zzbbbbppppiiiivvvvvxxxxx",
            "111111110000010011zzbbbbppppiiiivvvvvxxxxx",
            "111111110000010100zzbbbbppppiiiivvvvvxxxxx",
            "111111110000010101zzbbbbppppiiiivvvvvxxxxx",
            "111111110000010110zzbbbbppppiiiivvvvvxxxxx",
            "111111110000010111zzbbbbppppiiiivvvvvxxxxx",
        ]
        scatter = [
            "111111110000011000zz0bbbbppppiiiissssvvvvv",
            "111111110000011001000000ppppiiiivvvvvxxxxx",
            "111111110000011001000001ppppiiiivvvvvxxxxx",
            "111111110000011010zzbbbbppppiiiivvvvvxxxxx",
            "111111110000011011zzbbbbppppiiiivvvvvxxxxx",
            "111111110000011100zzbbbbppppiiiivvvvvxxxxx",
            "111111110000011101zzbbbbppppiiiivvvvvxxxxx",
            "111111110000011110zzbbbbppppiiiivvvvvxxxxx",
            "111111110000011111zzbbbbppppiiiivvvvvxxxxx",
        ]
        gather_forms = [self.forms[f"xxlong.vgather1.v{number}"] for number in range(239, 248)]
        scatter_forms = [self.forms[f"xxlong.vscatter1.v{number}"] for number in range(248, 257)]
        self.assertEqual([pattern(form) for form in gather_forms], gather)
        self.assertEqual([pattern(form) for form in scatter_forms], scatter)
        self.assertEqual(
            [form.fixed_required_bytes for form in gather_forms],
            [6, 6, 6, 6, 6, 7, 8, 10, 14],
        )
        self.assertEqual(
            [form.fixed_required_bytes for form in scatter_forms],
            [6, 6, 6, 6, 6, 7, 8, 10, 14],
        )
        self.assertTrue(all(
            form.control.repeat.rep and not form.control.repeat.repcc
            for form in gather_forms + scatter_forms
        ))

        self.assertEqual(
            pattern(self.forms["long.vlcnt.v20"]),
            "11111010011000zz000001rrrr",
        )
        self.assertEqual(
            pattern(self.forms["long.vlcadd.v21"]),
            "11111010011000zz000010rrrr",
        )
        self.assertEqual(self.forms["long.vlcadd.v21"].fixed_required_bytes, 5)
        retired = {"RDVL", "RDCNT", "ADDVL", "ADDPL"}
        self.assertTrue(retired.isdisjoint(form.mnemonic for form in self.ir.forms))

    def test_flags_annotations_and_repeat_observations_follow_complete_contracts(self) -> None:
        for operation in self.ir.operations:
            for case in operation.cases:
                for bank in case.flags or ():
                    self.assertEqual(
                        tuple(effect.flag for effect in bank.effects),
                        defs_schema.FLAG_BANK_FLAGS[bank.bank],
                        operation.id,
                    )
        for form in self.ir.forms:
            operation = next(
                operation
                for operation in self.ir.operations
                if form.key in operation.forms
            )
            self.assertEqual(
                form.annotations,
                decode_ir._operation_annotations(operation, form.key),
                form.key,
            )
            self.assertNotEqual(form.control.repeat.observed_kind, "flags", form.key)
        self.assertEqual(
            self.forms["short.cmp_x_rn_s_rn_d"].control.repeat.observed_kind,
            "computed",
        )
        self.assertEqual(
            self.forms["medium.adc_x_rn_s_rn_d"].control.repeat.observed_kind,
            "result",
        )

    def test_fea_forms_expose_every_possible_conversion_cause(self) -> None:
        conversion_causes = {"NV", "OF", "UF", "NX"}
        fpu_cases = [
            case
            for operation in self.ir.operations
            if operation.execution_route == "fpu"
            for case in operation.cases
        ]
        self.assertTrue(fpu_cases)
        self.assertTrue(any(
            conversion_causes <= {
                effect.flag
                for bank in case.flags or ()
                if bank.bank == "FFLAGS"
                for effect in bank.effects
            }
            for case in fpu_cases
        ))

    def test_serialization_is_deterministic_and_json_friendly(self) -> None:
        first = decode_ir.decode_ir_json(self.ir)
        second = decode_ir.decode_ir_json(decode_ir.load_decode_ir())
        self.assertEqual(first, second)
        parsed = json.loads(first)
        self.assertEqual(parsed["limits"]["form_count"], len(parsed["forms"]))
        self.assertEqual(
            [operation["id"] for operation in parsed["operations"]],
            sorted(operation["id"] for operation in parsed["operations"]),
        )
        self.assertEqual(
            {form_id for operation in parsed["operations"] for form_id in operation["forms"]},
            {form["key"] for form in parsed["forms"]},
        )
        self.assertEqual(parsed["forms"][0]["index"], 0)
        self.assertEqual(parsed["forms"][0]["key"], self.ir.forms[0].key)

    def test_owner_validation_rejects_direct_live_ir_invariant_breaks(self) -> None:
        first = self.ir.forms[0]
        duplicate_index = self.replace_form(replace(first, index=1))
        duplicate_key = replace(
            self.ir,
            forms=(replace(first, key=self.ir.forms[1].key),) + self.ir.forms[1:],
        )
        bad_limits = replace(
            self.ir,
            limits=replace(self.ir.limits, max_operands=3),
        )

        encoded_form = next(
            form
            for form in self.ir.forms
            if any(
                isinstance(operand.source, decode_ir.EncodedFieldSourceIR)
                for operand in form.operands
            )
        )
        operand_index = next(
            index
            for index, operand in enumerate(encoded_form.operands)
            if isinstance(operand.source, decode_ir.EncodedFieldSourceIR)
        )
        broken_operand = replace(
            encoded_form.operands[operand_index],
            source=decode_ir.EncodedFieldSourceIR("missing", (0,)),
        )
        broken_operands = (
            encoded_form.operands[:operand_index]
            + (broken_operand,)
            + encoded_form.operands[operand_index + 1 :]
        )
        missing_field = self.replace_form(replace(encoded_form, operands=broken_operands))

        layout_form = self.forms["medium.add_q_imm64_ea_e"]
        bad_layout = self.replace_form(
            replace(layout_form, layout=tuple(reversed(layout_form.layout)))
        )

        incomplete_ea = replace(
            self.ir,
            effective_addresses=replace(
                self.ir.effective_addresses,
                compact_entries=self.ir.effective_addresses.compact_entries[:-1],
            ),
        )

        families = {
            family.name: family
            for family in self.ir.effective_addresses.descriptor_families
        }
        ext1, ext2 = families["ext1"], families["ext2"]
        bad_length_ea = replace(
            self.ir.effective_addresses,
            descriptor_families=tuple(
                replace(family, descriptor_bytes=2)
                if family.name == "ext1" else family
                for family in self.ir.effective_addresses.descriptor_families
            ),
        )
        bad_descriptor_length = replace(self.ir, effective_addresses=bad_length_ea)

        ext2_form = ext2.forms[0]
        descriptor_positions = ext2_form.fields[0].positions
        bad_field = replace(
            ext2_form.fields[0],
            positions=(ext2_form.width,) + descriptor_positions[1:],
        )
        bad_ext2_form = replace(
            ext2_form,
            fields=(bad_field,) + ext2_form.fields[1:],
        )
        bad_field_ea = replace(
            self.ir.effective_addresses,
            descriptor_families=tuple(
                replace(family, forms=(bad_ext2_form,) + ext2.forms[1:])
                if family.name == "ext2" else family
                for family in self.ir.effective_addresses.descriptor_families
            ),
        )
        bad_descriptor_field = replace(self.ir, effective_addresses=bad_field_ea)

        for label, broken in (
            ("dense index", duplicate_index),
            ("stable key", duplicate_key),
            ("derived slot limits", bad_limits),
            ("source field", missing_field),
            ("layout order", bad_layout),
            ("compact completeness", incomplete_ea),
            ("descriptor length", bad_descriptor_length),
            ("descriptor field range", bad_descriptor_field),
        ):
            with self.subTest(label=label), self.assertRaises(ValueError):
                decode_ir.validate_decode_ir(broken)


if __name__ == "__main__":
    unittest.main()
