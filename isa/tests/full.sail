function test_full_decode() -> unit = {
  test_event_boundaries();
  test_fp_semantics();
  assert(operation_count(all_semantic_operations()) == 205);
  assert(count_non_fp_operations(all_semantic_operations()) == 145);
  assert(verify_representative_records(representative_form_records()) == 484);
  assert(verify_no_generic_external_fallback(representative_form_records()) == 484);
  assert(verify_fp_first_phase(representative_form_records()) == 115);
  let local_state = {
    initial_cpu() with registers = one_registers(), supervisor = true,
                       status = 0x0000000000000010,
                       fp_enabled = true, fptrans_enabled = true
  };
  assert(verify_local_representatives(representative_form_records(), local_state) == 484);
  assert(verify_non_fp_routes(representative_form_records(), local_state) == 307);
  test_local_integer_boundaries();
  test_divide_bounds_and_conditions();
  test_state_register_local();
  test_typed_decode_and_transactions();
  test_non_fp_typed_families();
  test_protocol_audit();

  match decode_full_record([|0xCF, 0xC6, 0x08, 0x20, 0x7F, 0xFE|]) {
    Some(instruction) => {
      assert(instruction.form.form_id == "medium.add_x_imm8s_ea_e");
      expect_operand_value(instruction, "src", 0x00000000000000FE);
      expect_ea_payload(instruction, "dst", 0x000000000000007F, 8)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xD3, 0xE0, 0xD0, 0x31, 0x7F, 0x34, 0x12|]) {
    Some(instruction) => {
      assert(instruction.form.form_id == "long.mov_x_ea_s_ea_d");
      expect_ea_payload(instruction, "src", 0x000000000000007F, 8);
      expect_ea_payload(instruction, "dst", 0x0000000000001234, 16)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCD, 0xEC, 0x05, 0x92, 0x02, 0x7F|]) {
    Some(instruction) => match first_ea_operand(instruction.operands) {
      Some(operand) => match operand.ea {
        Some(ea) => {
          assert(ea.descriptor_name == "explicit_segment_index");
          expect_ea_field(ea.fields, "s", 1);
          expect_ea_field(ea.fields, "b", 0);
          expect_ea_field(ea.fields, "i", 2);
          assert(ea.payload == 0x000000000000007F)
        },
        None() => assert(false),
      },
      None() => assert(false),
    },
    None() => assert(false),
  };

  match (decode_full_record([|0x70|]), decode_full_record([|0x77|]),
         decode_full_record([|0x78|]), decode_full_record([|0x7F|])) {
    (Some(push_first), Some(push_last), Some(pop_first), Some(pop_last)) => {
      expect_operand_value(push_first, "pair_id", 0x0000000000000000);
      expect_operand_value(push_last, "pair_id", 0x0000000000000007);
      expect_operand_value(pop_first, "pair_id", 0x0000000000000000);
      expect_operand_value(pop_last, "pair_id", 0x0000000000000007);
      assert(pair_first_index(0) == 0);
      assert(pair_first_index(7) == 14);
      assert_pair_mapping(0)
    },
    _ => assert(false),
  };

  match decode_full_record([|0x0E|]) {
    Some(instruction) => {
      expect_operand_value(instruction, "imm", 0x0000000000000008);
      let state = { initial_cpu() with sp = 0x0000000000000100 };
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(not_bool(result.awaiting_environment));
      assert(result.state.sp == 0x0000000000000108)
    },
    None() => assert(false),
  }
}
