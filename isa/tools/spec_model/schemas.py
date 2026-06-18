from __future__ import annotations

from typing import Any

from .core import (
    KeySchema,
    SpecError,
    check_allowed_keys,
    check_list_items,
    check_mapping_item_keys,
    check_mapping_values,
    check_optional_mapping,
    is_scalar_value,
    schema_keys,
)

class LocalInstructionSchema(KeySchema):
    name = "local instruction fragment"
    keys = {
        "mnemonic",
        "doc",
        "behavior",
        "attributes",
        "allocation",
        "forms",
    }


class LocalDocSchema(KeySchema):
    name = "local instruction documentation"
    keys = {
        "title",
        "summary",
        "description",
        "instruction_family",
        "instruction_class",
    }


LOCAL_OPERATION_BY_MNEMONIC_KEYS = {
    "inputs": "inputs_by_mnemonic",
    "input_output": "input_output_by_mnemonic",
    "flags": "flags_by_mnemonic",
    "fp_flags": "fp_flags_by_mnemonic",
    "privilege": "privilege_by_mnemonic",
    "memory": "memory_by_mnemonic",
    "serializing": "serializing_by_mnemonic",
    "signedness": "signedness_by_mnemonic",
    "bounds_mode": "bounds_mode_by_mnemonic",
    "interval": "interval_by_mnemonic",
    "destination_size": "destination_size_by_mnemonic",
    "output": "output_by_mnemonic",
    "count_rules": "count_rules_by_mnemonic",
    "flag_rules": "flag_rules_by_mnemonic",
    "control_register_access": "control_register_access_by_mnemonic",
}


LOCAL_OPERATION_CANONICAL_KEYS = set(LOCAL_OPERATION_BY_MNEMONIC_KEYS.values())
LOCAL_BEHAVIOR_KEYS = {
    "group",
    "operation",
    "operation_by_form",
    "inputs",
    "input_output",
    "output",
    "signedness",
    "bounds_mode",
    "interval",
    "destination_size",
    "count_rules",
    "flag_rules",
    "control_register_access",
    "banked_forms",
    "long_transfer_operands",
    "atomic_cs_pc_commit",
    "canonicalization",
    "descriptor_payloads",
}
LOCAL_ATTRIBUTE_KEYS = {
    "flags",
    "fp_flags",
    "privilege",
    "memory",
    "memory_ordering",
    "atomic",
    "serializing",
    "cpuid_feature",
    "prefix_availability",
    "repeatable",
    "streaming_candidate",
}
REP_OBSERVED_VALUE_RULES = {
    "src_value",
    "rhs_minus_lhs",
    "lhs_bitwise_and_rhs",
    "result_value",
}
REPFLAGS_RULES = {
    "flags_logic_observed_value",
    "flags_sub_rhs_lhs",
    "fpu_compare_flags",
    "fpu_interval_v_flag",
}
MEMORY_RULES = {
    "at_most_one_memory_operand",
    "memory_memory_explicit_form",
    "bulk_extend_memory_memory",
    "addressable_memory_operand_required",
    "encinst_destination_memory_operand",
}
MEMORY_MEMORY_DEFAULT_RULES = {"operation_opt_in"}


def check_mapping_list_items(
    value: Any,
    path: str,
    allowed: type[KeySchema],
    errors: list[str],
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{path}[{index}] must be a mapping")
            continue
        check_allowed_keys(item, f"{path}[{index}]", allowed, errors)


def check_flat_operand_list(value: Any, path: str, errors: list[str]) -> None:
    check_mapping_list_items(value, path, OperandSchema, errors)


def check_operand_alternatives(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    if not value:
        return
    if all(isinstance(item, dict) for item in value):
        check_flat_operand_list(value, path, errors)
        return
    if all(isinstance(item, list) for item in value):
        for index, alternative in enumerate(value):
            check_flat_operand_list(alternative, f"{path}[{index}]", errors)
        return
    errors.append(f"{path} must be either an operand list or a list of operand-list alternatives")


class RegistersRootSchema(KeySchema):
    name = "registers root"
    keys = {
        "version",
        "register_classes",
        "data_register_banking",
        "special_register_classes",
        "control_register_classes",
        "floating_point_register_model",
        "special_registers",
        "translation_control",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_mapping_values(value.get("register_classes", {}), f"{path}.register_classes", RegisterClassSchema, errors)
        check_mapping_values(value.get("special_register_classes", {}), f"{path}.special_register_classes", SpecialRegisterClassSchema, errors)
        for name, body in (value.get("special_register_classes") or {}).items():
            if isinstance(body, dict):
                check_list_items(body.get("encoding", []), f"{path}.special_register_classes.{name}.encoding", SpecialRegisterEncodingSchema, errors)
        check_mapping_values(value.get("control_register_classes", {}), f"{path}.control_register_classes", ControlRegisterClassSchema, errors)
        for name, body in (value.get("control_register_classes") or {}).items():
            if not isinstance(body, dict):
                continue
            check_list_items(body.get("selector_groups", []), f"{path}.control_register_classes.{name}.selector_groups", ControlSelectorGroupSchema, errors)
            for index, group in enumerate(body.get("selector_groups", []) or []):
                if isinstance(group, dict):
                    check_list_items(group.get("selectors", []), f"{path}.control_register_classes.{name}.selector_groups[{index}].selectors", ControlSelectorSchema, errors)
        check_list_items(value.get("special_registers", []), f"{path}.special_registers", SpecialRegisterSchema, errors)
        for index, reg in enumerate(value.get("special_registers", []) or []):
            if isinstance(reg, dict):
                check_named_field_map(reg.get("layout"), f"{path}.special_registers[{index}].layout", errors)
        DataRegisterBankingSchema.validate(value.get("data_register_banking"), f"{path}.data_register_banking", errors)
        FloatingPointRegisterModelSchema.validate(value.get("floating_point_register_model"), f"{path}.floating_point_register_model", errors)
        TranslationControlSchema.validate(value.get("translation_control"), f"{path}.translation_control", errors)


class SegmentsRootSchema(KeySchema):
    name = "segments root"
    keys = {"version", "segment_registers", "layout", "disabled_when", "semantics"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_list_items(value.get("segment_registers", []), f"{path}.segment_registers", SegmentRegisterSchema, errors)
        layout = value.get("layout")
        if isinstance(layout, dict):
            check_mapping_values(layout, f"{path}.layout", SegmentLayoutFieldSchema, errors)
        check_optional_mapping(value.get("disabled_when"), f"{path}.disabled_when", SegmentDisabledWhenSchema, errors)
        semantics = value.get("semantics")
        check_optional_mapping(semantics, f"{path}.semantics", SegmentSemanticsSchema, errors)
        if not isinstance(semantics, dict):
            return
        check_optional_mapping(semantics.get("bounds_only_mode"), f"{path}.semantics.bounds_only_mode", SegmentBoundsOnlyModeSchema, errors)
        check_optional_mapping(semantics.get("formulas"), f"{path}.semantics.formulas", SegmentFormulasSchema, errors)
        check_optional_mapping(semantics.get("arithmetic"), f"{path}.semantics.arithmetic", SegmentArithmeticSchema, errors)
        check_optional_mapping(semantics.get("modes"), f"{path}.semantics.modes", SegmentModesSchema, errors)


class PrefixesRootSchema(KeySchema):
    name = "prefixes root"
    keys = {"version", "prefix_word", "prefixes", "mutually_exclusive_groups"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_allowed_keys(value.get("prefix_word"), f"{path}.prefix_word", PrefixWordSchema, errors)
        check_list_items(value.get("prefixes"), f"{path}.prefixes", PrefixEntrySchema, errors)
        for index, prefix in enumerate(value.get("prefixes", []) or []):
            if not isinstance(prefix, dict):
                continue
            prefix_path = f"{path}.prefixes[{index}]"
            for key, allowed in (
                ("syntax", PrefixSyntaxSchema),
                ("condition", PrefixConditionSchema),
                ("operand", PrefixOperandSchema),
                ("requires", PrefixRequiresSchema),
                ("counter_encoding", PrefixCounterEncodingSchema),
                ("indexed_ea_counter_use", PrefixIndexedEaCounterUseSchema),
                ("fast_contract_alias", PrefixFastContractAliasSchema),
                ("alignment", PrefixAlignmentSchema),
                ("encoding_scope", PrefixEncodingScopeSchema),
                ("fault_behavior", PrefixFaultBehaviorSchema),
            ):
                if key in prefix:
                    check_allowed_keys(prefix[key], f"{prefix_path}.{key}", allowed, errors)
            fault = prefix.get("fault_behavior")
            if isinstance(fault, dict) and isinstance(fault.get("continuation_state"), dict):
                continuation = fault["continuation_state"]
                check_allowed_keys(continuation, f"{prefix_path}.fault_behavior.continuation_state", PrefixContinuationStateSchema, errors)
                if isinstance(continuation.get("group_start"), dict):
                    check_allowed_keys(continuation["group_start"], f"{prefix_path}.fault_behavior.continuation_state.group_start", PrefixContinuationGroupStartSchema, errors)
                if isinstance(continuation.get("counter_register"), dict):
                    check_allowed_keys(continuation["counter_register"], f"{prefix_path}.fault_behavior.continuation_state.counter_register", PrefixContinuationCounterRegisterSchema, errors)


class ConditionsRootSchema(KeySchema):
    name = "conditions root"
    keys = {"version", "conditions"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if isinstance(value, dict):
            check_list_items(value.get("conditions", []), f"{path}.conditions", ConditionSchema, errors)


class EffectiveAddressRootSchema(KeySchema):
    name = "effective-address root"
    keys = {
        "version",
        "fields",
        "ea_forms",
        "reserved_forms_behavior",
        "reserved_forms",
        "extended_ea_descriptor",
        "extended_ea_forms",
        "manual_text",
        "immediate_rules",
        "indexed_ea_rules",
        "update_eligible",
        "update_ineligible",
        "ea_coverage_audit",
        "ea_operand_policy",
        "instruction_ea_constraints",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_mapping_values(value.get("fields", {}), f"{path}.fields", EaFieldSchema, errors)
        ea_forms = value.get("ea_forms") or {}
        if isinstance(ea_forms, dict):
            check_allowed_keys(ea_forms, f"{path}.ea_forms", EaFormsSchema, errors)
            check_list_items(ea_forms.get("compact", []), f"{path}.ea_forms.compact", CompactEaFormSchema, errors)
        check_list_items(value.get("extended_ea_forms", []), f"{path}.extended_ea_forms", ExtendedEaFormSchema, errors)
        manual_text = value.get("manual_text")
        check_optional_mapping(manual_text, f"{path}.manual_text", EaManualTextSchema, errors)
        check_list_items(value.get("reserved_forms", []), f"{path}.reserved_forms", ReservedEaFormSchema, errors)
        compact_forms = value.get("ea_forms", {}).get("compact", []) if isinstance(value.get("ea_forms"), dict) else []
        for index, form in enumerate(compact_forms):
            if isinstance(form, dict) and isinstance(form.get("operands"), list):
                check_list_items(form["operands"], f"{path}.ea_forms.compact[{index}].operands", CompactEaOperandSchema, errors)
        descriptor = value.get("extended_ea_descriptor")
        check_optional_mapping(descriptor, f"{path}.extended_ea_descriptor", ExtendedEaDescriptorSchema, errors)
        if isinstance(descriptor, dict):
            check_mapping_item_keys(descriptor.get("fields"), f"{path}.extended_ea_descriptor.fields", EaDescriptorFieldSchema, errors)
            check_optional_mapping(descriptor.get("reserved_modes"), f"{path}.extended_ea_descriptor.reserved_modes", EaReservedModesSchema, errors)
            check_optional_mapping(descriptor.get("reserved_segment_field"), f"{path}.extended_ea_descriptor.reserved_segment_field", EaReservedSegmentFieldSchema, errors)
            check_mapping_item_keys(descriptor.get("compact_escapes"), f"{path}.extended_ea_descriptor.compact_escapes", EaCompactEscapeSchema, errors)
        immediate = value.get("immediate_rules") or {}
        if isinstance(immediate, dict):
            check_mapping_values(immediate, f"{path}.immediate_rules", EaImmediateRuleSchema, errors)
        indexed = value.get("indexed_ea_rules")
        check_optional_mapping(indexed, f"{path}.indexed_ea_rules", IndexedEaRulesSchema, errors)
        if isinstance(indexed, dict):
            check_optional_mapping(indexed.get("scale_syntax"), f"{path}.indexed_ea_rules.scale_syntax", EaScaleSyntaxSchema, errors)
            check_optional_mapping(indexed.get("rep_counter_index"), f"{path}.indexed_ea_rules.rep_counter_index", EaRepCounterIndexSchema, errors)
        for key in ("update_eligible", "update_ineligible"):
            check_optional_mapping(value.get(key), f"{path}.{key}", EaUpdateSetSchema, errors)
        audit = value.get("ea_coverage_audit") or {}
        check_optional_mapping(audit, f"{path}.ea_coverage_audit", EaCoverageAuditSchema, errors)
        if isinstance(audit, dict):
            check_mapping_item_keys(audit.get("required_properties"), f"{path}.ea_coverage_audit.required_properties", EaAuditPropertySchema, errors)
        policy = value.get("ea_operand_policy") or {}
        check_optional_mapping(policy, f"{path}.ea_operand_policy", EaOperandPolicySchema, errors)
        if isinstance(policy, dict):
            check_mapping_item_keys(policy.get("ea_sets"), f"{path}.ea_operand_policy.ea_sets", EaSetSchema, errors)
            check_mapping_item_keys(policy.get("extended_form_constraints"), f"{path}.ea_operand_policy.extended_form_constraints", EaExtendedFormConstraintSchema, errors)
        constraints = value.get("instruction_ea_constraints") or {}
        if isinstance(constraints, dict):
            check_mapping_values(constraints, f"{path}.instruction_ea_constraints", InstructionEaConstraintSchema, errors)


class InstructionsRootSchema(KeySchema):
    name = "instructions root"
    keys = {
        "version",
        "operand_schema",
        "canonical_aliases",
        "instruction_docs",
        "save_area_formats",
        "operation_semantics",
        "allocation",
        "families",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        InstructionOperandSchemaDeclaration.validate(value.get("operand_schema"), f"{path}.operand_schema", errors)
        check_list_items(value.get("canonical_aliases", []), f"{path}.canonical_aliases", CanonicalAliasSchema, errors)
        check_mapping_values(value.get("instruction_docs", {}), f"{path}.instruction_docs", InstructionDocSchema, errors)
        check_mapping_values(value.get("save_area_formats", {}), f"{path}.save_area_formats", SaveAreaFormatSchema, errors)
        families = value.get("families") or {}
        if isinstance(families, dict):
            for family_name, family in families.items():
                if not isinstance(family, dict):
                    continue
                family_path = f"{path}.families.{family_name}"
                check_allowed_keys(family, family_path, InstructionFamilySchema, errors)
                for section_name in ("compact_primary", "integer", "system", "fpu"):
                    if section_name not in family:
                        continue
                    check_mapping_values(family[section_name], f"{family_path}.{section_name}", CatalogEntrySchema, errors)
                    for entry_key, entry in (family[section_name] or {}).items():
                        if isinstance(entry, dict):
                            CatalogEntrySchema.validate(entry, f"{family_path}.{section_name}.{entry_key}", errors)
        InstructionAllocationSchema.validate(value.get("allocation"), f"{path}.allocation", errors)
        operation = value.get("operation_semantics") or {}
        if isinstance(operation, dict):
            OperationSemanticsRootSchema.validate(operation, f"{path}.operation_semantics", errors)


class OpcodesRootSchema(KeySchema):
    name = "opcodes root"
    keys = {
        "version",
        "word_size",
        "max_instruction_words",
        "word0",
        "sentinels",
        "reserved",
        "canonical_rules",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if isinstance(value, dict):
            check_list_items(value.get("sentinels", []), f"{path}.sentinels", OpcodeSentinelSchema, errors)
            check_list_items(value.get("canonical_rules", []), f"{path}.canonical_rules", OpcodeCanonicalRuleSchema, errors)


class SemanticsRootSchema(KeySchema):
    name = "semantics root"
    keys = {"version", "encoding_rules", "compatibility_rules"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        encoding = value.get("encoding_rules")
        check_optional_mapping(encoding, f"{path}.encoding_rules", SemanticsEncodingRulesSchema, errors)
        if isinstance(encoding, dict):
            length = encoding.get("instruction_length") or {}
            check_optional_mapping(length, f"{path}.encoding_rules.instruction_length", InstructionLengthSchema, errors)
            if isinstance(length, dict):
                check_optional_mapping(length.get("overlong_encoding"), f"{path}.encoding_rules.instruction_length.overlong_encoding", OverlongEncodingSchema, errors)
                check_optional_mapping(length.get("undersized_encoding"), f"{path}.encoding_rules.instruction_length.undersized_encoding", UndersizedEncodingSchema, errors)
            check_optional_mapping(encoding.get("memory_operands"), f"{path}.encoding_rules.memory_operands", MemoryOperandsSchema, errors)
            update = encoding.get("address_update_prefix") or {}
            check_optional_mapping(update, f"{path}.encoding_rules.address_update_prefix", AddressUpdatePrefixSchema, errors)
            if isinstance(update, dict):
                check_optional_mapping(update.get("applies_to"), f"{path}.encoding_rules.address_update_prefix.applies_to", AddressUpdateAppliesToSchema, errors)
            check_optional_mapping(encoding.get("repeat_prefixes"), f"{path}.encoding_rules.repeat_prefixes", RepeatPrefixesEncodingSchema, errors)
            check_mapping_item_keys(encoding.get("canonical_forms"), f"{path}.encoding_rules.canonical_forms", CanonicalFormSchema, errors)
            long_transfer = encoding.get("long_control_transfer") or {}
            check_optional_mapping(long_transfer, f"{path}.encoding_rules.long_control_transfer", LongControlTransferSchema, errors)
            if isinstance(long_transfer, dict):
                check_optional_mapping(long_transfer.get("segment_immediate_plus_offset_immediate"), f"{path}.encoding_rules.long_control_transfer.segment_immediate_plus_offset_immediate", SegmentImmediateOffsetSchema, errors)

        compatibility = value.get("compatibility_rules")
        check_optional_mapping(compatibility, f"{path}.compatibility_rules", SemanticsCompatibilityRulesSchema, errors)
        if not isinstance(compatibility, dict):
            return
        reserved = compatibility.get("reserved_bits") or {}
        check_optional_mapping(reserved, f"{path}.compatibility_rules.reserved_bits", ReservedBitsSchema, errors)
        if isinstance(reserved, dict):
            for key in ("architected_register_bits", "control_register_bits"):
                check_optional_mapping(reserved.get(key), f"{path}.compatibility_rules.reserved_bits.{key}", ReservedRegisterBitsSchema, errors)
            check_optional_mapping(reserved.get("selector_values"), f"{path}.compatibility_rules.reserved_bits.selector_values", ReservedSelectorValuesSchema, errors)
            check_optional_mapping(reserved.get("page_table_bits"), f"{path}.compatibility_rules.reserved_bits.page_table_bits", ReservedPageTableBitsSchema, errors)
            check_optional_mapping(reserved.get("interrupt_vector_table_bits"), f"{path}.compatibility_rules.reserved_bits.interrupt_vector_table_bits", ReservedInterruptVectorTableBitsSchema, errors)
            check_optional_mapping(reserved.get("supervisor_frame_bits"), f"{path}.compatibility_rules.reserved_bits.supervisor_frame_bits", ReservedSupervisorFrameBitsSchema, errors)
            check_optional_mapping(reserved.get("software_defined_bits"), f"{path}.compatibility_rules.reserved_bits.software_defined_bits", SoftwareDefinedBitsSchema, errors)
        faults = compatibility.get("instruction_encoding_faults") or {}
        if isinstance(faults, dict):
            check_mapping_values(faults, f"{path}.compatibility_rules.instruction_encoding_faults", InstructionEncodingFaultSchema, errors)
        prefix_values = compatibility.get("prefix_values") or {}
        check_optional_mapping(prefix_values, f"{path}.compatibility_rules.prefix_values", PrefixValuesCompatibilitySchema, errors)
        if isinstance(prefix_values, dict):
            check_optional_mapping(prefix_values.get("unassigned"), f"{path}.compatibility_rules.prefix_values.unassigned", PrefixUnassignedValuesSchema, errors)
        canonical = compatibility.get("canonical_encodings") or {}
        check_optional_mapping(canonical, f"{path}.compatibility_rules.canonical_encodings", CanonicalEncodingsSchema, errors)
        if isinstance(canonical, dict):
            check_optional_mapping(canonical.get("noncanonical_default"), f"{path}.compatibility_rules.canonical_encodings.noncanonical_default", NoncanonicalDefaultSchema, errors)
            check_optional_mapping(canonical.get("explicit_alias_or_priority"), f"{path}.compatibility_rules.canonical_encodings.explicit_alias_or_priority", ExplicitAliasOrPrioritySchema, errors)
        cpuid = compatibility.get("cpuid") or {}
        check_optional_mapping(cpuid, f"{path}.compatibility_rules.cpuid", CpuidCompatibilitySchema, errors)
        if isinstance(cpuid, dict):
            for key in ("unknown_class", "unknown_leaf", "unknown_index"):
                check_optional_mapping(cpuid.get(key), f"{path}.compatibility_rules.cpuid.{key}", CpuidUnknownResultSchema, errors)
            check_optional_mapping(cpuid.get("reserved_result_bits"), f"{path}.compatibility_rules.cpuid.reserved_result_bits", CpuidReservedResultBitsSchema, errors)
            check_optional_mapping(cpuid.get("runtime_mutability"), f"{path}.compatibility_rules.cpuid.runtime_mutability", CpuidRuntimeMutabilitySchema, errors)


class InterruptsRootSchema(KeySchema):
    name = "interrupts root"
    keys = {
        "version",
        "privileged_programming_model",
        "exception_processing",
        "interrupt_vector_assignment",
        "interrupt_vector_table",
        "supervisor_stack_frame",
        "reset_state",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        privileged = value.get("privileged_programming_model")
        check_optional_mapping(privileged, f"{path}.privileged_programming_model", PrivilegedProgrammingModelSchema, errors)
        if isinstance(privileged, dict):
            check_list_items(privileged.get("normative_rules", []), f"{path}.privileged_programming_model.normative_rules", NormativeRuleSchema, errors)
            check_optional_mapping(privileged.get("privilege_state"), f"{path}.privileged_programming_model.privilege_state", PrivilegeStateSchema, errors)
            check_optional_mapping(privileged.get("entry_status_policy"), f"{path}.privileged_programming_model.entry_status_policy", EntryStatusPolicySchema, errors)
            check_optional_mapping(privileged.get("syscall"), f"{path}.privileged_programming_model.syscall", SyscallModelSchema, errors)
            check_optional_mapping(privileged.get("interrupt_exception_entry"), f"{path}.privileged_programming_model.interrupt_exception_entry", InterruptExceptionEntrySchema, errors)
            check_optional_mapping(privileged.get("return_rules"), f"{path}.privileged_programming_model.return_rules", ReturnRulesSchema, errors)
            check_optional_mapping(privileged.get("interrupt_nesting"), f"{path}.privileged_programming_model.interrupt_nesting", InterruptNestingSchema, errors)
            check_optional_mapping(privileged.get("control_register_access"), f"{path}.privileged_programming_model.control_register_access", ControlRegisterAccessSchema, errors)

        exception = value.get("exception_processing")
        check_optional_mapping(exception, f"{path}.exception_processing", ExceptionProcessingSchema, errors)
        if isinstance(exception, dict):
            check_optional_mapping(exception.get("collapsed_fault_classes"), f"{path}.exception_processing.collapsed_fault_classes", CollapsedFaultClassesSchema, errors)

        assignment = value.get("interrupt_vector_assignment")
        check_optional_mapping(assignment, f"{path}.interrupt_vector_assignment", InterruptVectorAssignmentSchema, errors)
        if isinstance(assignment, dict):
            check_list_items(assignment.get("ranges", []), f"{path}.interrupt_vector_assignment.ranges", InterruptVectorRangeSchema, errors)
            check_list_items(assignment.get("vectors", []), f"{path}.interrupt_vector_assignment.vectors", InterruptVectorSchema, errors)

        table = value.get("interrupt_vector_table")
        check_optional_mapping(table, f"{path}.interrupt_vector_table", InterruptVectorTableSchema, errors)
        if isinstance(table, dict):
            layout = table.get("entry_layout") or {}
            check_optional_mapping(layout, f"{path}.interrupt_vector_table.entry_layout", InterruptVectorTableEntryLayoutSchema, errors)
            if isinstance(layout, dict):
                check_optional_mapping(layout.get("handler_address"), f"{path}.interrupt_vector_table.entry_layout.handler_address", InterruptVectorHandlerAddressSchema, errors)
                control = layout.get("control_byte") or {}
                check_optional_mapping(control, f"{path}.interrupt_vector_table.entry_layout.control_byte", InterruptVectorControlByteSchema, errors)
                if isinstance(control, dict):
                    check_named_field_map(control.get("fields"), f"{path}.interrupt_vector_table.entry_layout.control_byte.fields", errors)
                check_optional_mapping(layout.get("reserved"), f"{path}.interrupt_vector_table.entry_layout.reserved", InterruptVectorReservedBytesSchema, errors)

        frame = value.get("supervisor_stack_frame")
        SupervisorStackFrameSchema.validate(frame, f"{path}.supervisor_stack_frame", errors)


class CpuidRootSchema(KeySchema):
    name = "cpuid root"
    keys = {"version", "cpuid"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        cpuid = value.get("cpuid") or {}
        if not isinstance(cpuid, dict):
            return
        check_allowed_keys(cpuid, f"{path}.cpuid", CpuidObjectSchema, errors)
        check_list_items(cpuid.get("classes", []), f"{path}.cpuid.classes", CpuidClassSchema, errors)
        calling = cpuid.get("calling_convention")
        check_optional_mapping(calling, f"{path}.cpuid.calling_convention", CpuidCallingConventionSchema, errors)
        if isinstance(calling, dict):
            selector = calling.get("query_selector") or {}
            check_optional_mapping(selector, f"{path}.cpuid.calling_convention.query_selector", CpuidQuerySelectorSchema, errors)
            if isinstance(selector, dict):
                check_list_items(selector.get("bits", []), f"{path}.cpuid.calling_convention.query_selector.bits", BitFieldSchema, errors)
        policy = cpuid.get("policy")
        check_optional_mapping(policy, f"{path}.cpuid.policy", CpuidPolicySchema, errors)
        if isinstance(policy, dict):
            check_optional_mapping(policy.get("base_profile"), f"{path}.cpuid.policy.base_profile", CpuidBaseProfileSchema, errors)
            check_optional_mapping(policy.get("optional_extensions"), f"{path}.cpuid.policy.optional_extensions", CpuidOptionalExtensionsSchema, errors)
            check_optional_mapping(policy.get("implementation_properties"), f"{path}.cpuid.policy.implementation_properties", CpuidImplementationPropertiesSchema, errors)
        for class_index, cpuid_class in enumerate(cpuid.get("classes", []) or []):
            if not isinstance(cpuid_class, dict):
                continue
            for leaf_index, leaf in enumerate(cpuid_class.get("leaves", []) or []):
                if not isinstance(leaf, dict):
                    continue
                leaf_path = f"{path}.cpuid.classes[{class_index}].leaves[{leaf_index}]"
                CpuidLeafSchema.validate(leaf, leaf_path, errors)


class TerminologyRootSchema(KeySchema):
    name = "terminology root"
    keys = {"summary", "display_labels", "groups"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if isinstance(value, dict):
            check_list_items(value.get("groups", []), f"{path}.groups", TerminologyGroupSchema, errors)
            labels = value.get("display_labels", {})
            if not isinstance(labels, dict):
                errors.append(f"{path}.display_labels must be a mapping")
            else:
                for key, item in labels.items():
                    if not isinstance(key, str) or not isinstance(item, str):
                        errors.append(f"{path}.display_labels entries must map strings to strings")
                        break


ROOT_SCHEMAS = {
    "registers": RegistersRootSchema,
    "segments": SegmentsRootSchema,
    "prefixes": PrefixesRootSchema,
    "conditions": ConditionsRootSchema,
    "ea": EffectiveAddressRootSchema,
    "instructions": InstructionsRootSchema,
    "opcodes": OpcodesRootSchema,
    "semantics": SemanticsRootSchema,
    "interrupts": InterruptsRootSchema,
    "cpuid": CpuidRootSchema,
    "terminology": TerminologyRootSchema,
}


class SpecDocumentSchema(KeySchema):
    name = "complete ISA spec document"
    keys = set(ROOT_SCHEMAS)

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        if not isinstance(value, dict):
            errors.append(f"{path} must be a mapping")
            return
        for section, schema in ROOT_SCHEMAS.items():
            schema.validate(value.get(section), f"{section}.yaml", errors)

    @classmethod
    def validate_or_raise(cls, value: dict[str, Any]) -> None:
        errors: list[str] = []
        cls.validate(value, "spec", errors)
        if errors:
            joined = "\n- ".join(errors)
            raise SpecError(f"schema validation failed:\n- {joined}")


class PrefixEntrySchema(KeySchema):
    name = "prefix entry"
    keys = {
        "name",
        "value",
        "pattern",
        "group",
        "semantics",
        "applies_to",
        "requires",
        "syntax",
        "description",
        "condition",
        "operand",
        "eligible_operation_attribute",
        "fpu_conditional_mnemonics",
        "excluded_categories",
        "indexed_ea_counter_use",
        "counter_encoding",
        "observed_value",
        "observed_value_descriptions",
        "repflags",
        "repflags_descriptions",
        "counter_direction",
        "commit_rule",
        "streaming_candidate_attribute",
        "excluded_instruction_classes",
        "fast_contract_alias",
        "alignment",
        "encoding_scope",
        "fflags_accumulation",
        "fault_behavior",
    }


class PrefixSyntaxSchema(KeySchema):
    name = "prefix syntax"
    keys = {
        "mnemonic_template",
        "fast_contract_template",
        "condition_suffix",
        "dot_suffix_reserved_for_instruction_size",
        "applies_to_following_instruction",
        "separator",
        "examples",
        "aliases",
        "block",
        "block_template",
        "fast_contract_block_template",
        "applies_to_grouped_instructions",
        "terminator_prefix",
        "assembler_generated",
        "closes",
        "operand_annotation",
        "default_domain",
    }


class CatalogEntrySchema(KeySchema):
    name = "instruction catalog entry"
    keys = {
        "mnemonics",
        "operands",
        "compact_forms",
        "extended_forms",
        "form",
        "size",
        "source_size",
        "D_size",
        "A_size",
        "prefixes",
        "result",
        "reads",
        "writes",
        "updates",
        "memory_memory",
        "memory_destination_arithmetic",
        "memory_operands",
        "rounding",
        "nan_policy",
        "unordered",
        "conversions",
        "alias_of",
        "canonical_disassembly",
        "vector",
        "bitmap",
        "valid_bits",
        "performs_page_walk",
        "no_memory_access",
        "canonical_check",
        "page_walk",
        "if_trace_disabled",
        "compact",
        "zero_input",
        "access_width",
        "aliases",
        "disallow_segment_immediate",
        "disallow_update_prefix",
        "dst_ea_set",
        "encoding_fields",
        "extension_family",
        "implicit_inputs",
        "implicit_outputs",
        "input",
        "invalid_sizes",
        "note",
        "output",
        "size_per_register",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        if "operands" in value:
            check_operand_alternatives(value["operands"], f"{path}.operands", errors)
        for form_key in ("compact_forms", "extended_forms"):
            forms = value.get(form_key)
            if forms is None:
                continue
            if not isinstance(forms, list):
                errors.append(f"{path}.{form_key} must be a list")
                continue
            for index, form in enumerate(forms):
                if not isinstance(form, dict):
                    errors.append(f"{path}.{form_key}[{index}] must be a mapping")
                    continue
                check_allowed_keys(form, f"{path}.{form_key}[{index}]", InstructionFormSchema, errors)
                if "operands" in form:
                    check_flat_operand_list(form["operands"], f"{path}.{form_key}[{index}].operands", errors)


class OperationGroupSchema(KeySchema):
    name = "operation semantics group"
    keys = {
        "members",
        "inputs",
        "inputs_by_mnemonic",
        "input_output",
        "input_output_by_mnemonic",
        "output",
        "output_by_mnemonic",
        "flags",
        "flags_by_mnemonic",
        "fp_flags_by_mnemonic",
        "privilege",
        "privilege_by_mnemonic",
        "memory",
        "memory_by_mnemonic",
        "memory_ordering",
        "atomic",
        "serializing_by_mnemonic",
        "traps",
        "signedness_by_mnemonic",
        "bounds_mode_by_mnemonic",
        "bounds_mode_names",
        "interval_by_mnemonic",
        "destination_size_by_mnemonic",
        "source_size_suffix",
        "source_sizes_by_destination",
        "count_rules",
        "count_rules_by_mnemonic",
        "flag_rules",
        "flag_rules_by_mnemonic",
        "control_register_access_by_mnemonic",
        "bitmap",
        "banked_forms",
        "long_transfer_operands",
        "atomic_cs_pc_commit",
        "stack_segment",
        "stack_register",
        "canonicalization",
        "descriptor_payloads",
        "cpuid_feature",
        "implementation",
    }


class LocalAllocationSchema(KeySchema):
    name = "local instruction allocation"
    keys = {"catalog_section", "layout_group"}


class InstructionFormSchema(KeySchema):
    name = "instruction form"
    keys = {
        "operands",
        "size",
        "compact",
        "constraint",
        "memory_memory",
        "flags",
        "force_size_suffix",
        "extension_family",
        "allocation_cluster",
        "profile",
    }


class OperandSchema(KeySchema):
    name = "operand"
    keys = {"name", "type"}


class BitFieldSchema(KeySchema):
    name = "bit field"
    keys = {"bit", "bits", "range", "name", "description", "values"}


class DescribedFieldSchema(KeySchema):
    name = "described field"
    keys = {"description"}


class InstructionAllocationSchema(KeySchema):
    name = "instruction allocation policy"
    keys = {
        "mnemonic_policy",
        "frequency_model",
        "extension_roots",
        "extension_family_rules",
        "primary_clusters",
        "condition_field",
        "field_reclaim",
        "field_layout",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        if value is None:
            return
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_optional_mapping(value.get("mnemonic_policy"), f"{path}.mnemonic_policy", InstructionMnemonicPolicySchema, errors)
        frequency = value.get("frequency_model")
        check_optional_mapping(frequency, f"{path}.frequency_model", InstructionFrequencyModelSchema, errors)
        if isinstance(frequency, dict):
            check_list_items(frequency.get("rules", []), f"{path}.frequency_model.rules", InstructionFrequencyRuleSchema, errors)
            for index, rule in enumerate(frequency.get("rules", []) or []):
                if isinstance(rule, dict) and isinstance(rule.get("match"), dict):
                    check_allowed_keys(rule["match"], f"{path}.frequency_model.rules[{index}].match", InstructionFrequencyRuleMatchSchema, errors)
        check_optional_mapping(value.get("extension_roots"), f"{path}.extension_roots", InstructionExtensionRootsSchema, errors)
        check_list_items(value.get("extension_family_rules", []), f"{path}.extension_family_rules", InstructionExtensionFamilyRuleSchema, errors)
        for index, rule in enumerate(value.get("extension_family_rules", []) or []):
            if isinstance(rule, dict) and isinstance(rule.get("match"), dict):
                check_allowed_keys(rule["match"], f"{path}.extension_family_rules[{index}].match", InstructionExtensionFamilyRuleMatchSchema, errors)
        check_optional_mapping(value.get("primary_clusters"), f"{path}.primary_clusters", InstructionPrimaryClustersSchema, errors)
        condition = value.get("condition_field") or {}
        check_optional_mapping(condition, f"{path}.condition_field", InstructionConditionFieldSchema, errors)
        if isinstance(condition, dict):
            check_optional_mapping(condition.get("reclaim_never_taken"), f"{path}.condition_field.reclaim_never_taken", InstructionConditionReclaimSchema, errors)
        field_reclaim = value.get("field_reclaim") or {}
        check_optional_mapping(field_reclaim, f"{path}.field_reclaim", InstructionFieldReclaimSchema, errors)
        if isinstance(field_reclaim, dict):
            check_list_items(field_reclaim.get("invalid_values", []), f"{path}.field_reclaim.invalid_values", InstructionFieldReclaimInvalidValueSchema, errors)
            for index, rule in enumerate(field_reclaim.get("invalid_values", []) or []):
                if isinstance(rule, dict) and isinstance(rule.get("match"), dict):
                    check_allowed_keys(rule["match"], f"{path}.field_reclaim.invalid_values[{index}].match", InstructionFieldReclaimInvalidValueMatchSchema, errors)
        field_layout = value.get("field_layout") or {}
        check_optional_mapping(field_layout, f"{path}.field_layout", InstructionFieldLayoutSchema, errors)
        if isinstance(field_layout, dict):
            check_optional_mapping(
                field_layout.get("anchor_strategy"),
                f"{path}.field_layout.anchor_strategy",
                InstructionFieldLayoutAnchorStrategySchema,
                errors,
            )
            check_optional_mapping(field_layout.get("field_score"), f"{path}.field_layout.field_score", InstructionFieldScoreSchema, errors)
            check_list_items(field_layout.get("subfield_affinities", []), f"{path}.field_layout.subfield_affinities", InstructionSubfieldAffinitySchema, errors)


class SemanticsEncodingRulesSchema(KeySchema):
    name = "encoding rules"
    keys = {
        "instruction_length",
        "memory_operands",
        "address_update_prefix",
        "repeat_prefixes",
        "canonical_forms",
        "long_control_transfer",
    }


class SemanticsCompatibilityRulesSchema(KeySchema):
    name = "compatibility rules"
    keys = {
        "reserved_bits",
        "instruction_encoding_faults",
        "prefix_values",
        "canonical_encodings",
        "cpuid",
    }


class LocalBehaviorSchema(KeySchema):
    name = "local instruction behavior"
    keys = LOCAL_BEHAVIOR_KEYS


class LocalAttributesSchema(KeySchema):
    name = "local instruction attributes"
    keys = LOCAL_ATTRIBUTE_KEYS


class PrefixWordSchema(KeySchema):
    name = "prefix word"
    keys = {
        "bytes_per_instruction",
        "fill_order",
        "decode_order",
        "unused_slot_encoding",
        "conflict_resolution",
        "conflict_note",
    }


class PrefixConditionSchema(KeySchema):
    name = "prefix condition"
    keys = {"type", "field", "values_from", "full_set"}


class PrefixOperandSchema(KeySchema):
    name = "prefix operand"
    keys = {"type", "field", "range", "role"}


class PrefixRequiresSchema(KeySchema):
    name = "prefix requires"
    keys = {"update_eligible_ea"}


class PrefixCounterEncodingSchema(KeySchema):
    name = "prefix counter encoding"
    keys = {
        "interpretation",
        "value_bits",
        "zero_rule",
        "index_value",
        "update_after_condition_true_iteration",
        "condition_false_iteration_counter_rule",
        "update_after_successful_group_iteration",
        "completion_rule",
        "fault_restart_rule",
        "update_on_faulting_iteration",
    }


class PrefixIndexedEaCounterUseSchema(KeySchema):
    name = "prefix indexed EA counter use"
    keys = {"allowed", "counter_value", "example", "note"}


class PrefixFastContractAliasSchema(KeySchema):
    name = "prefix fast contract alias"
    keys = {"mnemonic", "emits", "contract"}


class PrefixAlignmentSchema(KeySchema):
    name = "prefix alignment"
    keys = {"grouping_window_bytes"}


class PrefixEncodingScopeSchema(KeySchema):
    name = "prefix encoding scope"
    keys = {"group_termination"}


class PrefixFaultBehaviorSchema(KeySchema):
    name = "prefix fault behavior"
    keys = {
        "precise_at",
        "commit_rule",
        "faulting_instruction_rule",
        "later_grouped_instructions",
        "continuation_state",
    }


class PrefixContinuationStateSchema(KeySchema):
    name = "prefix continuation state"
    keys = {"saved_pc", "group_start", "counter_register"}


class PrefixContinuationGroupStartSchema(KeySchema):
    name = "prefix continuation group start"
    keys = {"bits", "range_words"}


class PrefixContinuationCounterRegisterSchema(KeySchema):
    name = "prefix continuation counter register"
    keys = {"bits"}


class InstructionOperandSchemaDeclaration(KeySchema):
    name = "instruction operand schema declaration"
    keys = {
        "role_name_pattern",
        "condition_role",
        "selector_roles",
        "types",
        "size_codes",
        "size_kinds",
        "named_values",
        "bitmap_operands",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_mapping_values(value.get("size_codes", {}), f"{path}.size_codes", SizeCodeSchema, errors)
        check_mapping_values(value.get("size_kinds", {}), f"{path}.size_kinds", SizeKindSchema, errors)
        for name, kind in (value.get("size_kinds") or {}).items():
            if isinstance(kind, dict):
                check_list_items(kind.get("values", []), f"{path}.size_kinds.{name}.values", SizeKindValueSchema, errors)
                check_list_items(kind.get("reserved_values", []), f"{path}.size_kinds.{name}.reserved_values", ReservedNamedValueSchema, errors)
        check_mapping_values(value.get("named_values", {}), f"{path}.named_values", NamedValueSetSchema, errors)
        for name, named in (value.get("named_values") or {}).items():
            if isinstance(named, dict):
                check_list_items(named.get("values", []), f"{path}.named_values.{name}.values", NamedValueSchema, errors)
                check_list_items(named.get("reserved_values", []), f"{path}.named_values.{name}.reserved_values", ReservedNamedValueSchema, errors)
        check_mapping_values(value.get("bitmap_operands", {}), f"{path}.bitmap_operands", BitmapOperandSchema, errors)
        for name, bitmap in (value.get("bitmap_operands") or {}).items():
            if isinstance(bitmap, dict):
                check_list_items(bitmap.get("ranges", []), f"{path}.bitmap_operands.{name}.ranges", BitmapOperandRangeSchema, errors)


class SizeCodeSchema(KeySchema):
    name = "instruction size code"
    keys = {"suffix", "bytes", "label"}


class SizeKindSchema(KeySchema):
    name = "instruction size kind"
    keys = {"field", "values", "reserved_values"}


class SizeKindValueSchema(KeySchema):
    name = "instruction size kind value"
    keys = {"value", "code"}


class NamedValueSetSchema(KeySchema):
    name = "named operand value set"
    keys = {"width", "values", "reserved_values"}


class NamedValueSchema(KeySchema):
    name = "named operand value"
    keys = {"value", "name", "description"}


class ReservedNamedValueSchema(KeySchema):
    name = "reserved named operand value"
    keys = {"value", "name", "description"}


class BitmapOperandSchema(KeySchema):
    name = "bitmap operand"
    keys = {"width", "ranges"}


class BitmapOperandRangeSchema(KeySchema):
    name = "bitmap operand register range"
    keys = {"bits", "register_class"}


class CanonicalAliasSchema(KeySchema):
    name = "canonical alias"
    keys = {"alias", "target", "condition", "canonical_disassembly", "required_target_forms"}


class InstructionDocSchema(KeySchema):
    name = "instruction documentation entry"
    keys = {
        "title",
        "summary",
        "description",
        "instruction_family",
        "instruction_class",
    }


class SaveAreaFormatSchema(KeySchema):
    name = "save area format"
    keys = {
        "title",
        "applies_to",
        "fixed_base_bytes",
        "fixed_slots",
        "base_bitmap_bits",
        "instruction_behavior",
        "extension_components",
        "extension_component_order",
        "extension_component_formats",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        if "fixed_slots" in value:
            check_mapping_list_items(value["fixed_slots"], f"{path}.fixed_slots", SaveAreaFixedSlotSchema, errors)
        bitmap = value.get("base_bitmap_bits")
        if bitmap is not None:
            SaveAreaBitmapSchema.validate(bitmap, f"{path}.base_bitmap_bits", errors)
        if "extension_component_formats" in value:
            check_mapping_list_items(
                value["extension_component_formats"],
                f"{path}.extension_component_formats",
                SaveAreaExtensionComponentSchema,
                errors,
            )
            if isinstance(value["extension_component_formats"], list):
                for index, component in enumerate(value["extension_component_formats"]):
                    if isinstance(component, dict):
                        SaveAreaExtensionComponentSchema.validate(
                            component,
                            f"{path}.extension_component_formats[{index}]",
                            errors,
                        )


class SaveAreaFixedSlotSchema(KeySchema):
    name = "save area fixed slot"
    keys = {"offset", "field"}


class SaveAreaBitmapSchema(KeySchema):
    name = "save area bitmap"
    keys = {"description", "reserved_bits", "mappings"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        if "mappings" in value:
            check_mapping_list_items(value["mappings"], f"{path}.mappings", SaveAreaBitmapMappingSchema, errors)


class SaveAreaBitmapMappingSchema(KeySchema):
    name = "save area bitmap mapping"
    keys = {"bits", "slot", "meaning"}


class SaveAreaExtensionComponentSchema(KeySchema):
    name = "save area extension component"
    keys = {
        "component_id",
        "name",
        "title",
        "extension_requirement",
        "validity",
        "description",
        "size",
        "component_bitmap_bits",
        "slots",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        bitmap = value.get("component_bitmap_bits")
        if bitmap is not None:
            SaveAreaBitmapSchema.validate(bitmap, f"{path}.component_bitmap_bits", errors)
        if "slots" in value:
            check_mapping_list_items(value["slots"], f"{path}.slots", SaveAreaComponentSlotSchema, errors)
            if isinstance(value["slots"], list):
                for index, slot in enumerate(value["slots"]):
                    if isinstance(slot, dict):
                        SaveAreaComponentSlotSchema.validate(slot, f"{path}.slots[{index}]", errors)


class SaveAreaComponentSlotSchema(KeySchema):
    name = "save area component slot"
    keys = {"offset", "field", "meaning", "repeat"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        if "repeat" in value:
            check_optional_mapping(value.get("repeat"), f"{path}.repeat", SaveAreaComponentSlotRepeatSchema, errors)


class SaveAreaComponentSlotRepeatSchema(KeySchema):
    name = "save area component slot repeat"
    keys = {"count", "offset_start", "offset_stride", "field_template", "meaning_template"}


class InstructionFamilySchema(KeySchema):
    name = "instruction family"
    keys = {"category", "registers", "compact_primary", "integer", "system", "fpu"}


class OperationSemanticsRootSchema(KeySchema):
    name = "operation semantics root"
    keys = {
        "version",
        "status",
        "notation",
        "defaults",
        "syntax_policy",
        "operation_attributes",
        "prefix_availability",
        "repeat_prefixes",
        "group_order",
        "groups",
        "instructions",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_optional_mapping(value.get("defaults"), f"{path}.defaults", OperationDefaultsSchema, errors)
        check_optional_mapping(value.get("syntax_policy"), f"{path}.syntax_policy", OperationSyntaxPolicySchema, errors)
        syntax_policy = value.get("syntax_policy") or {}
        if isinstance(syntax_policy, dict):
            check_optional_mapping(syntax_policy.get("condition_code"), f"{path}.syntax_policy.condition_code", ConditionCodeSyntaxSchema, errors)
        attrs = value.get("operation_attributes") or {}
        check_optional_mapping(attrs, f"{path}.operation_attributes", OperationAttributesSchema, errors)
        if isinstance(attrs, dict):
            for name in ("repeatable_operation", "streaming_candidate"):
                check_optional_mapping(attrs.get(name), f"{path}.operation_attributes.{name}", OperationAttributeSchema, errors)
        prefix_availability = value.get("prefix_availability")
        if isinstance(prefix_availability, dict):
            check_mapping_values(prefix_availability, f"{path}.prefix_availability", PrefixAvailabilitySchema, errors)
        if isinstance(value.get("groups"), dict):
            check_mapping_values(value["groups"], f"{path}.groups", OperationGroupSchema, errors)


class InstructionFrequencyModelSchema(KeySchema):
    name = "instruction allocation frequency model"
    keys = {"description", "default_weight_by_category", "rules"}


class InstructionMnemonicPolicySchema(KeySchema):
    name = "instruction allocation mnemonic policy"
    keys = {
        "core_control_compact_mnemonics",
        "cache_management_mnemonics",
        "tlb_management_mnemonics",
        "fence_mnemonics",
        "integer_minmax_order",
        "integer_mul_div_compact_order",
    }


class InstructionFrequencyRuleSchema(KeySchema):
    name = "instruction allocation frequency rule"
    keys = {"id", "match", "weight", "compact", "reason"}


class InstructionFrequencyRuleMatchSchema(KeySchema):
    name = "instruction allocation frequency rule match"
    keys = {"mnemonic", "profile", "size", "category", "semantic_family"}


class InstructionExtensionRootsSchema(KeySchema):
    name = "instruction allocation extension roots"
    keys = {"group_by", "condition_field_in_primary", "preferred_region", "allow_low_payload_roots"}


class InstructionExtensionFamilyRuleSchema(KeySchema):
    name = "instruction extension family rule"
    keys = {"match", "extension_family"}


class InstructionExtensionFamilyRuleMatchSchema(KeySchema):
    name = "instruction extension family rule match"
    keys = {"group", "profile"}


class InstructionPrimaryClustersSchema(KeySchema):
    name = "instruction primary clusters"
    keys = {"order"}


class InstructionConditionFieldSchema(KeySchema):
    name = "instruction condition field"
    keys = {"reclaim_never_taken"}


class InstructionConditionReclaimSchema(KeySchema):
    name = "instruction condition field reclaim"
    keys = {"mnemonics", "condition_value", "reason"}


class InstructionFieldReclaimSchema(KeySchema):
    name = "instruction field reclaim"
    keys = {"invalid_values"}


class InstructionFieldReclaimInvalidValueSchema(KeySchema):
    name = "instruction field reclaim invalid value"
    keys = {"match", "field_source", "values", "reason"}


class InstructionFieldReclaimInvalidValueMatchSchema(KeySchema):
    name = "instruction field reclaim invalid value match"
    keys = {"mnemonic", "profile", "size"}


class InstructionFieldLayoutSchema(KeySchema):
    name = "instruction field layout"
    keys = {"anchor_strategy", "explicit_signature_order", "field_score", "subfield_affinities"}


class InstructionFieldLayoutAnchorStrategySchema(KeySchema):
    name = "instruction field layout anchor strategy"
    keys = {"format_order", "placement", "fixed_signatures"}


class InstructionFieldScoreSchema(KeySchema):
    name = "instruction field score"
    keys = {"formula", "default_multiplier", "signature_multipliers"}


class InstructionSubfieldAffinitySchema(KeySchema):
    name = "instruction subfield affinity"
    keys = {
        "name",
        "container_signature",
        "subfield_signature",
        "offset",
        "width",
        "score_multiplier",
        "reason",
    }


class OperationDefaultsSchema(KeySchema):
    name = "operation semantics defaults"
    keys = {"unmentioned_flags", "overlong_encoding", "undersized_encoding", "memory_memory", "operand_evaluation_order"}


class OperationSyntaxPolicySchema(KeySchema):
    name = "operation syntax policy"
    keys = {"condition_code"}


class ConditionCodeSyntaxSchema(KeySchema):
    name = "condition-code syntax"
    keys = {"spelling", "placement", "dot_suffix_reserved_for", "applies_to"}


class OperationAttributesSchema(KeySchema):
    name = "operation attributes"
    keys = {"repeatable_operation", "streaming_candidate"}


class OperationAttributeSchema(KeySchema):
    name = "operation attribute"
    keys = {"integer", "fpu", "excluded_categories", "state_query_general_only"}


class PrefixAvailabilitySchema(KeySchema):
    name = "prefix availability"
    keys = {"table_code", "derived_from", "scope", "operation_attribute", "mnemonics"}


class EaFieldSchema(KeySchema):
    name = "EA field"
    keys = {"width"}


class EaFormsSchema(KeySchema):
    name = "EA forms root"
    keys = {"compact"}


class CompactEaFormSchema(KeySchema):
    name = "compact EA form"
    keys = {
        "name",
        "pattern",
        "class",
        "register_class",
        "syntax",
        "base",
        "memory",
        "ea_capable",
        "update_eligible",
        "displacement",
        "absolute",
        "signed",
        "sign_extension",
        "extra_words",
        "extension",
        "extension_class",
        "index_extension",
        "fixed_segment",
        "operands",
    }


class ExtendedEaFormSchema(KeySchema):
    name = "extended EA form"
    keys = {
        "name",
        "syntax",
        "class",
        "segment_selectable",
        "segment_field",
        "default_segment",
        "default_segment_syntax",
        "default_segment_allowed",
        "fixed_segment",
        "base",
        "index",
        "scale",
        "displacement",
        "absolute",
        "memory",
        "update_eligible",
        "extra_words",
        "value",
        "escape",
        "index_extension",
        "store_allowed",
    }


class EaManualTextSchema(KeySchema):
    name = "EA manual text"
    keys = {"form_descriptions", "payload_descriptions"}


class ReservedEaFormSchema(KeySchema):
    name = "reserved EA form"
    keys = {"name", "pattern"}


class CompactEaOperandSchema(KeySchema):
    name = "compact EA form operand"
    keys = {"type", "field", "width", "signed", "source", "words"}


class ExtendedEaDescriptorSchema(KeySchema):
    name = "extended EA descriptor"
    keys = {"fields", "segment_values", "reserved_modes", "reserved_segment_field", "compact_escapes"}


class EaDescriptorFieldSchema(KeySchema):
    name = "EA descriptor field"
    keys = {"bits"}


class EaReservedModesSchema(KeySchema):
    name = "EA reserved modes"
    keys = {"pattern", "exception"}


class EaReservedSegmentFieldSchema(KeySchema):
    name = "EA reserved segment field"
    keys = {"required_value", "exception"}


class EaCompactEscapeSchema(KeySchema):
    name = "EA compact escape"
    keys = {"ea_value", "index_extension"}


class EaImmediateRuleSchema(KeySchema):
    name = "EA immediate rule"
    keys = {"forms", "canonical_widths", "excluded_widths", "sign_extension", "memory_access", "ea_forms"}


class IndexedEaRulesSchema(KeySchema):
    name = "indexed EA rules"
    keys = {
        "signed_displacements",
        "default_segment_may_omit_prefix",
        "assembler_scale_required",
        "scale_syntax",
        "rep_counter_index",
    }


class EaScaleSyntaxSchema(KeySchema):
    name = "EA scale syntax"
    keys = {"rule", "examples", "invalid_examples"}


class EaRepCounterIndexSchema(KeySchema):
    name = "EA REP counter index"
    keys = {"allowed", "counter_value", "example"}


class EaUpdateSetSchema(KeySchema):
    name = "EA update set"
    keys = {"compact", "extended"}


class EaCoverageAuditSchema(KeySchema):
    name = "EA coverage audit"
    keys = {"required_compact_ea_forms", "required_extended_ea_forms", "required_properties"}


class EaAuditPropertySchema(KeySchema):
    name = "EA audit property"
    keys = set(CompactEaFormSchema.keys) | set(ExtendedEaFormSchema.keys)


class EaOperandPolicySchema(KeySchema):
    name = "EA operand policy"
    keys = {"default_allowed_ea_set", "ea_sets", "extended_form_constraints"}


class EaSetSchema(KeySchema):
    name = "EA set"
    keys = {"includes", "excludes", "inherits"}


class EaExtendedFormConstraintSchema(KeySchema):
    name = "EA extended form constraint"
    keys = {"includes", "excludes", "rationale"}


class InstructionEaConstraintSchema(KeySchema):
    name = "instruction EA constraint"
    keys = {
        "src_ea_set",
        "dst_ea_set",
        "lhs_ea_set",
        "rhs_ea_set",
        "target_ea_set",
        "memory_operand_ea_set",
        "allow_memory_memory",
        "require_memory_operand",
        "require_address_value",
        "no_memory_access",
        "segment_translation_only",
        "src",
        "dst",
        "disallow",
        "segment_operand",
        "atomic_cs_pc_update",
        "disallow_immediate_segment_plus_immediate_offset",
        "stack_register",
        "stack_segment",
        "disallow_update_prefix",
        "source_width",
        "destination_width",
    }


class RegisterClassSchema(KeySchema):
    name = "register class"
    keys = {"count", "width", "role", "allocatable"}


class SpecialRegisterClassSchema(KeySchema):
    name = "special register class"
    keys = {"width", "role", "registers", "encoding_bits", "reserved_values", "encoding"}


class SpecialRegisterEncodingSchema(KeySchema):
    name = "special register encoding"
    keys = {"value", "bits", "register"}


class ControlRegisterClassSchema(KeySchema):
    name = "control register class"
    keys = {"width", "role", "registers", "encoding_bits", "selector_groups", "reserved_selector_fault"}


class ControlSelectorGroupSchema(KeySchema):
    name = "control selector group"
    keys = {"name", "range", "selectors"}


class ControlSelectorSchema(KeySchema):
    name = "control selector"
    keys = {"value", "register"}


class SpecialRegisterSchema(KeySchema):
    name = "special register"
    keys = {
        "name",
        "width",
        "access_width",
        "access_size",
        "class",
        "role",
        "description",
        "note",
        "implicit",
        "privilege",
        "layout",
        "valid_bits",
        "nonzero_bits",
        "write_policy",
        "extension_requirement",
    }


class DataRegisterBankingSchema(KeySchema):
    name = "data register banking"
    keys = {"selector", "model", "tiers", "object_attribute"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_optional_mapping(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_optional_mapping(value.get("selector"), f"{path}.selector", DataRegisterBankingSelectorSchema, errors)
        selector = value.get("selector") or {}
        if isinstance(selector, dict):
            check_optional_mapping(selector.get("discovery"), f"{path}.selector.discovery", DataRegisterBankingDiscoverySchema, errors)
        check_optional_mapping(value.get("model"), f"{path}.model", DataRegisterBankingModelSchema, errors)
        check_list_items(value.get("tiers", []), f"{path}.tiers", DataRegisterBankingTierSchema, errors)


class DataRegisterBankingSelectorSchema(KeySchema):
    name = "data register banking selector"
    keys = {"name", "width", "architectural_namespace", "required_base_count", "discovery"}


class DataRegisterBankingDiscoverySchema(KeySchema):
    name = "data register banking discovery"
    keys = {"cpuid_class", "cpuid_leaf"}


class DataRegisterBankingModelSchema(KeySchema):
    name = "data register banking model"
    keys = {
        "visible_register_rule",
        "ordinary_instruction_rule",
        "bank_zero_role",
        "public_boundary_rule",
        "handler_entry_rule",
        "saved_state_rule",
    }


class DataRegisterBankingTierSchema(KeySchema):
    name = "data register banking tier"
    keys = {"name", "required_banks", "description"}


class FloatingPointRegisterModelSchema(KeySchema):
    name = "floating-point register model"
    keys = {"registers", "fflags", "fstatus", "unsupported_instruction_exception"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_optional_mapping(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_optional_mapping(value.get("registers"), f"{path}.registers", FloatingPointRegistersSchema, errors)
        check_optional_mapping(value.get("fflags"), f"{path}.fflags", FflagsSchema, errors)
        fflags = value.get("fflags") or {}
        if isinstance(fflags, dict):
            check_named_field_map(fflags.get("bits"), f"{path}.fflags.bits", errors)
        check_optional_mapping(value.get("fstatus"), f"{path}.fstatus", FstatusSchema, errors)
        fstatus = value.get("fstatus") or {}
        if isinstance(fstatus, dict):
            check_named_field_map(fstatus.get("fields"), f"{path}.fstatus.fields", errors)
            check_optional_mapping(fstatus.get("exception_rule"), f"{path}.fstatus.exception_rule", FstatusExceptionRuleSchema, errors)
            check_optional_mapping(fstatus.get("write_policy"), f"{path}.fstatus.write_policy", FstatusWritePolicySchema, errors)
            check_optional_mapping(fstatus.get("ieee_754_default"), f"{path}.fstatus.ieee_754_default", FstatusIeeeDefaultSchema, errors)


class FloatingPointRegistersSchema(KeySchema):
    name = "floating-point registers"
    keys = {"count", "width", "names", "scalar_formats"}


class FflagsSchema(KeySchema):
    name = "FFLAGS"
    keys = {"width", "storage", "reset", "access_width", "access_size", "description", "bits"}


class FstatusSchema(KeySchema):
    name = "FSTATUS"
    keys = {
        "width",
        "access_width",
        "access_size",
        "reset",
        "privilege",
        "extension_requirement",
        "description",
        "fields",
        "rounding_modes",
        "exception_rule",
        "write_policy",
        "ieee_754_default",
    }


class FstatusExceptionRuleSchema(KeySchema):
    name = "FSTATUS exception rule"
    keys = {"trap_enabled", "trap_disabled"}


class FstatusWritePolicySchema(KeySchema):
    name = "FSTATUS write policy"
    keys = {"reserved_bits", "reserved_write_exception", "description"}


class FstatusIeeeDefaultSchema(KeySchema):
    name = "FSTATUS IEEE 754 default"
    keys = {"reset_value", "rule"}


class TranslationControlSchema(KeySchema):
    name = "translation control"
    keys = {"PTCR", "ASCR", "page_table_entry", "ICR"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_optional_mapping(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        ptcr = value.get("PTCR") or {}
        check_optional_mapping(ptcr, f"{path}.PTCR", PtcrSchema, errors)
        if isinstance(ptcr, dict):
            check_list_items(ptcr.get("PABITS_SEL", []), f"{path}.PTCR.PABITS_SEL", PabitsSelectorSchema, errors)
            check_optional_mapping(ptcr.get("paging_modes"), f"{path}.PTCR.paging_modes", PagingModesSchema, errors)
        check_optional_mapping(value.get("ASCR"), f"{path}.ASCR", AscrSchema, errors)
        PageTableEntrySchema.validate(value.get("page_table_entry"), f"{path}.page_table_entry", errors)
        check_optional_mapping(value.get("ICR"), f"{path}.ICR", IcrSchema, errors)


class PtcrSchema(KeySchema):
    name = "PTCR"
    keys = {"PABITS_SEL", "paging_modes", "PE_0", "PE_1", "address_flow"}


class PabitsSelectorSchema(KeySchema):
    name = "PABITS selector"
    keys = {"selector", "physical_address_bits", "access_fault"}


class PagingModesSchema(KeySchema):
    name = "paging modes"
    keys = {"LA57_0", "LA57_1"}


class AscrSchema(KeySchema):
    name = "ASCR"
    keys = {"AE", "ASID"}


class PageTableEntrySchema(KeySchema):
    name = "page table entry"
    keys = {
        "low_attribute_bits",
        "ranges",
        "addressing_type",
        "cache_policy",
        "table_bit",
        "walk_level_rules",
        "non_leaf_attributes",
        "leaf_attributes",
        "permission_rules",
    }

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_optional_mapping(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_named_field_map(value.get("low_attribute_bits"), f"{path}.low_attribute_bits", errors)
        check_optional_mapping(value.get("ranges"), f"{path}.ranges", PageTableEntryRangesSchema, errors)
        check_optional_mapping(value.get("walk_level_rules"), f"{path}.walk_level_rules", PageTableWalkLevelRulesSchema, errors)
        check_mapping_item_keys(value.get("non_leaf_attributes"), f"{path}.non_leaf_attributes", DescribedFieldSchema, errors)
        check_mapping_item_keys(value.get("leaf_attributes"), f"{path}.leaf_attributes", DescribedFieldSchema, errors)
        check_list_items(value.get("permission_rules", []), f"{path}.permission_rules", PageTablePermissionRuleSchema, errors)


class PageTableEntryRangesSchema(KeySchema):
    name = "page table entry ranges"
    keys = {"architectural_low_attributes", "physical_frame_number", "software_defined"}


class PageTableWalkLevelRulesSchema(KeySchema):
    name = "page table walk level rules"
    keys = {"large_pages", "non_leaf_levels", "leaf_level"}


class PageTablePermissionRuleSchema(KeySchema):
    name = "page table permission rule"
    keys = {"mode", "condition", "result"}


class IcrSchema(KeySchema):
    name = "ICR"
    keys = {"MAX_IDEPTH_0", "MAX_IDEPTH_n"}


class SegmentLayoutFieldSchema(KeySchema):
    name = "segment layout field"
    keys = {"bits", "description", "unit_bytes", "field_name"}


class SegmentDisabledWhenSchema(KeySchema):
    name = "segment disabled condition"
    keys = {"mantissa"}


class SegmentSemanticsSchema(KeySchema):
    name = "segment semantics"
    keys = {
        "purpose",
        "not_a_protection_mechanism",
        "protection_and_final_translation",
        "translation_order_when_enabled",
        "enabled_when",
        "bounds_only_mode",
        "formulas",
        "arithmetic",
        "modes",
    }


class SegmentBoundsOnlyModeSchema(KeySchema):
    name = "segment bounds-only mode"
    keys = {"field", "effect"}


class SegmentFormulasSchema(KeySchema):
    name = "segment formulas"
    keys = {"base_byte_address", "limit_byte_address", "segment_size_bytes"}


class SegmentArithmeticSchema(KeySchema):
    name = "segment arithmetic"
    keys = {"domain", "overflow_rule"}


class SegmentModesSchema(KeySchema):
    name = "segment modes"
    keys = {"disabled", "translated_window", "bounds_only_window"}


class InstructionLengthSchema(KeySchema):
    name = "instruction length rule"
    keys = {"overlong_encoding", "undersized_encoding"}


class OverlongEncodingSchema(KeySchema):
    name = "overlong encoding rule"
    keys = {"behavior", "payload"}


class UndersizedEncodingSchema(KeySchema):
    name = "undersized encoding rule"
    keys = {"behavior", "rule"}


class MemoryOperandsSchema(KeySchema):
    name = "memory operands rule"
    keys = {"memory_memory_allowed_for", "default"}


class AddressUpdatePrefixSchema(KeySchema):
    name = "address update prefix rule"
    keys = {"applies_to", "disallowed_for"}


class AddressUpdateAppliesToSchema(KeySchema):
    name = "address update applies-to rule"
    keys = {"compact_ea_forms", "extended_ea_forms"}


class RepeatPrefixesEncodingSchema(KeySchema):
    name = "repeat prefixes encoding rule"
    keys = {"authoritative_source", "members"}


class CanonicalFormSchema(KeySchema):
    name = "canonical form rule"
    keys = {"canonical_form", "noncanonical_store_form"}


class LongControlTransferSchema(KeySchema):
    name = "long control transfer rule"
    keys = {
        "rationale",
        "disallow_general_CS_write",
        "segment_operand",
        "target_operand",
        "segment_immediate_plus_offset_immediate",
    }


class SegmentImmediateOffsetSchema(KeySchema):
    name = "segment immediate plus offset immediate rule"
    keys = {"allowed", "reason"}


class ReservedBitsSchema(KeySchema):
    name = "reserved bits compatibility rule"
    keys = {
        "architected_register_bits",
        "control_register_bits",
        "selector_values",
        "page_table_bits",
        "interrupt_vector_table_bits",
        "supervisor_frame_bits",
        "software_defined_bits",
    }


class ReservedRegisterBitsSchema(KeySchema):
    name = "reserved register bits"
    keys = {"read", "write", "write_exception"}


class ReservedSelectorValuesSchema(KeySchema):
    name = "reserved selector values"
    keys = {"exception"}


class ReservedPageTableBitsSchema(KeySchema):
    name = "reserved page table bits"
    keys = {"consumed_exception"}


class ReservedInterruptVectorTableBitsSchema(KeySchema):
    name = "reserved interrupt vector table bits"
    keys = {"write"}


class ReservedSupervisorFrameBitsSchema(KeySchema):
    name = "reserved supervisor frame bits"
    keys = {"write"}


class SoftwareDefinedBitsSchema(KeySchema):
    name = "software-defined bits"
    keys = {"hardware_use", "software_use"}


class InstructionEncodingFaultSchema(KeySchema):
    name = "instruction encoding fault"
    keys = {"exception", "defined"}


class PrefixValuesCompatibilitySchema(KeySchema):
    name = "prefix values compatibility rule"
    keys = {"unassigned"}


class PrefixUnassignedValuesSchema(KeySchema):
    name = "unassigned prefix values"
    keys = {"exception", "behavior", "reserved_for"}


class CanonicalEncodingsSchema(KeySchema):
    name = "canonical encodings compatibility rule"
    keys = {"assembler_default", "disassembler_default", "noncanonical_default", "explicit_alias_or_priority"}


class NoncanonicalDefaultSchema(KeySchema):
    name = "noncanonical default"
    keys = {"exception"}


class ExplicitAliasOrPrioritySchema(KeySchema):
    name = "explicit alias or priority"
    keys = {"allowed"}


class CpuidCompatibilitySchema(KeySchema):
    name = "CPUID compatibility rule"
    keys = {"unknown_class", "unknown_leaf", "unknown_index", "reserved_result_bits", "privilege", "serialization", "runtime_mutability"}


class CpuidUnknownResultSchema(KeySchema):
    name = "CPUID unknown result"
    keys = {"result"}


class CpuidReservedResultBitsSchema(KeySchema):
    name = "CPUID reserved result bits"
    keys = {"software_action"}


class CpuidRuntimeMutabilitySchema(KeySchema):
    name = "CPUID runtime mutability"
    keys = {"stable_after_reset"}


class PrivilegedProgrammingModelSchema(KeySchema):
    name = "privileged programming model"
    keys = {
        "normative_rules",
        "privilege_state",
        "entry_status_policy",
        "syscall",
        "interrupt_exception_entry",
        "return_rules",
        "interrupt_nesting",
        "control_register_access",
    }


class NormativeRuleSchema(KeySchema):
    name = "normative rule"
    keys = {"topic", "rule"}


class PrivilegeStateSchema(KeySchema):
    name = "privilege state"
    keys = {"PM", "access_domain"}


class EntryStatusPolicySchema(KeySchema):
    name = "entry status policy"
    keys = {"saved_status_return", "entry_status_changes", "entry_dbank_change", "interrupt_masking_on_entry", "note"}


class SyscallModelSchema(KeySchema):
    name = "syscall model"
    keys = {
        "vector",
        "entry_registers",
        "frame_style",
        "entry_table_size_bytes",
        "entry_address_alignment_bytes",
        "saved_state",
        "status_change",
        "dbank_change",
        "return_instruction",
        "return_policy",
    }


class InterruptExceptionEntrySchema(KeySchema):
    name = "interrupt and exception entry"
    keys = {
        "exception_model",
        "restart_policy",
        "status_change",
        "dbank_change",
        "interrupt_masking",
        "stack_selection",
        "nmi_stack_selection",
        "double_fault_stack_selection",
        "frame_save",
        "frame",
    }


class ReturnRulesSchema(KeySchema):
    name = "return rules"
    keys = {"SYSRET", "IRET", "malformed_frame"}


class InterruptNestingSchema(KeySchema):
    name = "interrupt nesting"
    keys = {"max_idepth_rule"}


class ControlRegisterAccessSchema(KeySchema):
    name = "control register access"
    keys = {"RDCR", "WRCR", "user_access_policy"}


class ExceptionProcessingSchema(KeySchema):
    name = "exception processing"
    keys = {
        "cpu_exception_model",
        "restart_policy",
        "interrupt_frame_save",
        "status_on_entry",
        "dbank_on_entry",
        "dbank_on_return",
        "handler_absent_behavior",
        "reserved_cpu_vector_behavior",
        "status_on_return",
        "malformed_return_frame",
        "iret_frame_type_check",
        "fault_priority",
        "collapsed_fault_classes",
        "address_fault_vector",
    }


class CollapsedFaultClassesSchema(KeySchema):
    name = "collapsed fault classes"
    keys = {"length_fault", "segment_fault", "canonical_address_fault"}


class InterruptVectorAssignmentSchema(KeySchema):
    name = "interrupt vector assignment"
    keys = {"policy", "syscall_vector", "syscall_entry", "ranges", "vectors"}


class InterruptVectorRangeSchema(KeySchema):
    name = "interrupt vector range"
    keys = {"range", "owner", "meaning"}


class InterruptVectorSchema(KeySchema):
    name = "interrupt vector"
    keys = {"vector", "name", "source", "frame_type"}


class InterruptVectorTableSchema(KeySchema):
    name = "interrupt vector table"
    keys = {"entries", "entry_size_bytes", "table_size_bytes", "base_address", "entry_index", "entry_layout"}


class InterruptVectorTableEntryLayoutSchema(KeySchema):
    name = "interrupt vector table entry layout"
    keys = {"handler_address", "control_byte", "reserved"}


class InterruptVectorHandlerAddressSchema(KeySchema):
    name = "interrupt vector handler address"
    keys = {"bytes", "width", "description"}


class InterruptVectorControlByteSchema(KeySchema):
    name = "interrupt vector control byte"
    keys = {"byte", "fields"}


class InterruptVectorReservedBytesSchema(KeySchema):
    name = "interrupt vector reserved bytes"
    keys = {"bytes", "description"}


class SupervisorStackFrameSchema(KeySchema):
    name = "supervisor stack frame"
    keys = {"slot_size_bytes", "base_size_bytes", "frame_size_unit_bytes", "description", "layout", "payload_slots", "repeat_fault_aux", "frame_types", "frame_info"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_optional_mapping(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_list_items(value.get("layout", []), f"{path}.layout", SupervisorStackFrameLayoutSlotSchema, errors)
        check_mapping_item_keys(value.get("payload_slots"), f"{path}.payload_slots", DescribedFieldSchema, errors)
        repeat = value.get("repeat_fault_aux") or {}
        check_optional_mapping(repeat, f"{path}.repeat_fault_aux", RepeatFaultAuxSchema, errors)
        if isinstance(repeat, dict):
            check_named_field_map(repeat.get("fields"), f"{path}.repeat_fault_aux.fields", errors)
            check_optional_mapping(repeat.get("formulas"), f"{path}.repeat_fault_aux.formulas", RepeatFaultAuxFormulasSchema, errors)
        check_list_items(value.get("frame_types", []), f"{path}.frame_types", FrameTypeSchema, errors)
        check_named_field_map(value.get("frame_info"), f"{path}.frame_info", errors)


class SupervisorStackFrameLayoutSlotSchema(KeySchema):
    name = "supervisor stack frame layout slot"
    keys = {"offset", "name", "description"}


class RepeatFaultAuxSchema(KeySchema):
    name = "repeat fault aux"
    keys = {"description", "fields", "formulas", "resume_rule"}


class RepeatFaultAuxFormulasSchema(KeySchema):
    name = "repeat fault aux formulas"
    keys = {"group_start_pc"}


class FrameTypeSchema(KeySchema):
    name = "frame type"
    keys = {"code", "name", "payload", "description"}


class CpuidCallingConventionSchema(KeySchema):
    name = "CPUID calling convention"
    keys = {
        "syntax",
        "input",
        "output",
        "query_selector",
        "unsupported_class",
        "unsupported_leaf",
        "unsupported_index",
        "privilege",
        "serialization",
        "reserved_result_bits",
        "runtime_mutability",
    }


class CpuidQuerySelectorSchema(KeySchema):
    name = "CPUID query selector"
    keys = {"bits"}


class CpuidPolicySchema(KeySchema):
    name = "CPUID policy"
    keys = {"base_profile", "optional_extensions", "implementation_properties"}


class CpuidBaseProfileSchema(KeySchema):
    name = "CPUID base profile"
    keys = {"name", "class", "description"}


class CpuidOptionalExtensionsSchema(KeySchema):
    name = "CPUID optional extensions"
    keys = {"class", "description", "unsupported_instruction_exception"}


class CpuidImplementationPropertiesSchema(KeySchema):
    name = "CPUID implementation properties"
    keys = {"class", "description"}


class CpuidLeafSchema(KeySchema):
    name = "CPUID leaf"
    keys = {"leaf", "name", "summary", "description", "topology_level_types", "results"}

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)
        if not isinstance(value, dict):
            return
        check_list_items(value.get("results", []), f"{path}.results", CpuidResultSchema, errors)
        for result_index, result in enumerate(value.get("results", []) or []):
            if isinstance(result, dict):
                check_list_items(result.get("bits", []), f"{path}.results[{result_index}].bits", BitFieldSchema, errors)


class CpuidResultSchema(KeySchema):
    name = "CPUID result"
    keys = {"index", "description", "bits", "extraction"}


class CpuidObjectSchema(KeySchema):
    name = "CPUID object"
    keys = {"calling_convention", "policy", "classes"}


class CpuidClassSchema(KeySchema):
    name = "CPUID class"
    keys = {"class", "name", "description", "leaves"}


class ConditionSchema(KeySchema):
    name = "condition"
    keys = {"name", "value", "aliases", "expression"}


class SegmentRegisterSchema(KeySchema):
    name = "segment register"
    keys = {"name", "selector", "width"}


class OpcodeSentinelSchema(KeySchema):
    name = "opcode sentinel"
    keys = {"id", "name", "pattern", "behavior", "override_decode", "privilege", "effects", "flags"}


class OpcodeCanonicalRuleSchema(KeySchema):
    name = "opcode canonical rule"
    keys = {"id", "when", "canonical", "noncanonical", "action"}


class TerminologyGroupSchema(KeySchema):
    name = "terminology group"
    keys = {"name", "terms"}


def check_named_field_map(value: Any, path: str, errors: list[str]) -> None:
    check_mapping_item_keys(value, path, BitFieldSchema, errors)
