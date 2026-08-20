function test_fp_metadata() -> unit = {
  assert(fp_operation_count(all_semantic_operations()) == 60);
  assert(fp_form_count(primary_form_catalog()) == 115);
  assert(fp_path_count(primary_form_catalog(), FpPathR) == 62);
  assert(fp_path_count(primary_form_catalog(), FpPathS1) == 36);
  assert(fp_path_count(primary_form_catalog(), FpPathS2) == 4);
  assert(fp_path_count(primary_form_catalog(), FpPathD1) == 11);
  assert(fp_path_count(primary_form_catalog(), FpPathStack) == 2);
  assert(fp_test_derived_form_count(primary_form_catalog()) == 115);

  match fp_find_form(primary_form_catalog(), "long.fclass_x_fn_s_rn_d") {
    Some(form) => {
      assert(fp_derive_result_kind(form, 4) == Some(FpResultInteger));
      assert(fp_derive_destination_kind(form) == FpDestinationRn)
    },
    None() => assert(false),
  };
  match fp_find_form(primary_form_catalog(),
                     "long.fsincosa_x_fn_s_fn_d_fn_c") {
    Some(form) => {
      assert(fp_derive_result_kind(form, 4) == Some(FpResultPair32));
      assert(fp_derive_result_kind(form, 8) == Some(FpResultPair64));
      assert(fp_derive_destination_kind(form) == FpDestinationFnPair)
    },
    None() => assert(false),
  };
  match fp_find_form(primary_form_catalog(), "medium.fxchg_fn_l_fn_r") {
    Some(form) => {
      assert(fp_derive_result_kind(form, 8) == Some(FpResultPairRaw64));
      assert(fp_derive_destination_kind(form) == FpDestinationFnPair)
    },
    None() => assert(false),
  }
}

function test_fp_operand_slots() -> unit = {
  let first = fp_test_operand32(0x000000003F800000);
  let second = fp_test_operand64(0x4000000000000000);
  let third = fp_test_raw64(0x1122334455667788);
  let empty = empty_fp_operand_slots();
  assert(fp_operand_valid_bitmap(empty) == 0b000);
  assert(fp_operand_slots_valid(empty, 0));
  match fp_operand_slot_set(empty, 0, first) {
    None() => assert(false),
    Some(one) => {
      assert(fp_operand_valid_bitmap(one) == 0b001);
      assert(fp_operand_slots_valid(one, 1));
      assert(fp_operand_slot_get(one, 0) == Some(first));
      match fp_operand_slot_set(one, 1, second) {
        None() => assert(false),
        Some(two) => {
          assert(fp_operand_valid_bitmap(two) == 0b011);
          assert(fp_operand_slots_valid(two, 2));
          match fp_operand_slot_set(two, 2, third) {
            Some(three) => {
              assert(fp_operand_valid_bitmap(three) == 0b111);
              assert(fp_operand_slots_valid(three, 3));
              assert(fp_operand_slot_get(three, 2) == Some(third))
            },
            None() => assert(false),
          }
        },
      }
    },
  };
  let hole : Fp_operand_slots = struct {
    operand0 = empty_fp_operand(), operand1 = second,
    operand2 = empty_fp_operand()
  };
  assert(fp_operand_valid_bitmap(hole) == 0b010);
  assert(not_bool(fp_operand_slots_valid(hole, 1)));
  assert(fp_operand_slot_get(empty, 3) == None());
  assert(fp_operand_slot_set(empty, -1, first) == None())
}

