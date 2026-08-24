function test_carry_record(bytes : list(bits(8)), width : int,
                           maximum : bits(64), signed_maximum : bits(64)) -> unit =
  match decode_full_record(bytes) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000000;
      state.registers[2] = maximum;
      state.flags = 0b0010;
      let carry = execute_full(instruction, state);
      assert(not_bool(carry.awaiting_environment));
      assert(carry.fault == None());
      assert(carry.state.registers[2] == 0x0000000000000000);
      assert(carry.state.flags == 0b1010);

      state.registers[2] = signed_maximum;
      let overflow = execute_full(instruction, state);
      assert(overflow.state.registers[2]
             == bits_from_int(tdiv_int(width_modulus(width), 2)));
      assert(overflow.state.flags == 0b0101)
    },
  }

function test_borrow_record(bytes : list(bits(8)), width : int,
                            maximum : bits(64)) -> unit =
  match decode_full_record(bytes) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000000;
      state.registers[2] = 0x0000000000000000;
      state.flags = 0b0010;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.fault == None());
      assert(result.state.registers[2] == maximum);
      assert(result.state.flags == 0b0110)
    },
  }

function test_zero_count_shift_record(bytes : list(bits(8)), expected_operation : Semantic_operation,
                                      input : bits(64), expected : bits(64)) -> unit =
  match decode_full_record(bytes) {
    None() => assert(false),
    Some(instruction) => {
      assert(instruction.form.operation == expected_operation);
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000020;
      state.registers[2] = input;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.fault == None());
      assert(result.state.registers[2] == expected)
    },
  }

function test_local_integer_boundaries() -> unit = {
  assert(canonical_register_result(Op_MOV, 0x1122334455667788, 1)
         == 0x0000000000000088);
  assert(canonical_register_result(Op_MOV, 0x1122334455667788, 2)
         == 0x0000000000007788);
  assert(canonical_register_result(Op_MOV, 0x1122334455667788, 4)
         == 0x0000000055667788);
  assert(canonical_register_result(Op_SAR, 0x0000000000000080, 1)
         == 0xFFFFFFFFFFFFFF80);

  test_carry_record([|0xC3, 0x08, 0x82|], 1, 0x00000000000000FF, 0x000000000000007F);
  test_carry_record([|0xC3, 0x18, 0x82|], 2, 0x000000000000FFFF, 0x0000000000007FFF);
  test_carry_record([|0xC3, 0x28, 0x82|], 4, 0x00000000FFFFFFFF, 0x000000007FFFFFFF);
  test_carry_record([|0xC3, 0x38, 0x82|], 8, 0xFFFFFFFFFFFFFFFF, 0x7FFFFFFFFFFFFFFF);
  test_borrow_record([|0xC3, 0x48, 0x82|], 1, 0x00000000000000FF);
  test_borrow_record([|0xC3, 0x58, 0x82|], 2, 0x000000000000FFFF);
  test_borrow_record([|0xC3, 0x68, 0x82|], 4, 0x00000000FFFFFFFF);
  test_borrow_record([|0xC3, 0x78, 0x82|], 8, 0xFFFFFFFFFFFFFFFF);

  assert(shift_result(Op_SHL, 0x0000000000000081, 0x0000000000000008, 1)
         == 0x0000000000000081);
  assert(shift_result(Op_SHR, 0x0000000000008001, 0x0000000000000010, 2)
         == 0x0000000000008001);
  assert(shift_result(Op_ROL, 0x0000000080000001, 0x0000000000000020, 4)
         == 0x0000000080000001);
  assert(shift_result(Op_ROR, 0x8000000000000001, 0x0000000000000040, 8)
         == 0x8000000000000001);
  assert(shift_result(Op_SAR, 0x0000000000000080, 0x0000000000000001, 1)
         == 0x00000000000000C0);
  test_zero_count_shift_record(
    [|0x94, 0x12|], Op_SHL, 0x1122334480000001, 0x0000000080000001
  );
  test_zero_count_shift_record(
    [|0x92, 0x12|], Op_SHR, 0x1122334480000001, 0x0000000080000001
  );
  test_zero_count_shift_record(
    [|0x98, 0x12|], Op_ROL, 0x1122334480000001, 0x0000000080000001
  );
  test_zero_count_shift_record(
    [|0x96, 0x12|], Op_ROR, 0x1122334480000001, 0x0000000080000001
  );
  test_zero_count_shift_record(
    [|0x9A, 0x12|], Op_SAR, 0x1122334480000001, 0xFFFFFFFF80000001
  );

  match decode_full_record([|0xC7, 0xEE, 0x64, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.flags = 0b1111;
      state.registers[0] = 0x11223344556677A5;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.state.registers[0] == 0x11223344556677A5);
      assert(result.state.flags == 0b1000)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC7, 0xEE, 0x3F, 0x80|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.flags = 0b1111;
      state.registers[0] = 0x80000000000000FF;
      let result = execute_full(instruction, state);
      assert(result.state.registers[0] == state.registers[0]);
      assert(result.state.flags == 0b1000)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x91, 0x22|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[2] = 0x0123456789ABCDEF;
      let result = execute_full(instruction, state);
      assert(result.state.registers[2] == 0x0000000089ABCDEF)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xC3, 0x31, 0x01|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000002;
      state.registers[2] = 0x8000000000000000;
      let result = execute_full(instruction, state);
      assert(result.state.registers[2] == 0x0000000000000001)
    },
    None() => assert(false),
  };
  assert(carryless_high(carryless_product(0x0000000000000080,
                                          0x0000000000000002), 1)
         == 0x0000000000000001);
  assert(carryless_high(carryless_product(0x0000000000008000,
                                          0x0000000000000002), 2)
         == 0x0000000000000001);
  assert(carryless_high(carryless_product(0x0000000080000000,
                                          0x0000000000000002), 4)
         == 0x0000000000000001);
  assert(carryless_high(carryless_product(0x8000000000000000,
                                          0x0000000000000002), 8)
         == 0x0000000000000001)
}

function test_setcc_direct_and_production() -> unit =
  match decode_full_record([|0xA0, 0x20|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_SETcc);
      assert(instruction.form.form_id == "short.setcc_rn_r");
      match find_operand_by_name("dst", instruction.operands) {
        Some(destination) => {
          let destination_index = unsigned(destination.value[3 .. 0]);
          var state = initial_cpu();
          state.registers[destination_index] = 0xFFFFFFFFFFFFFFFF;
          state.flags = 0b0000;
          assert(not_bool(predicate_holds(instruction, state)));
          match execute_SETcc(instruction, state) {
            Some(direct_false) => {
              let production_false = execute_full(instruction, state);
              assert(direct_false.fault == None());
              assert(production_false.fault == None());
              assert(not_bool(direct_false.awaiting_environment));
              assert(not_bool(production_false.awaiting_environment));
              assert(direct_false.pending.kind == CommitRegisters);
              assert(production_false.pending.kind == direct_false.pending.kind);
              assert(direct_false.state.registers[destination_index]
                     == 0x0000000000000000);
              assert(production_false.state.registers[destination_index]
                     == direct_false.state.registers[destination_index]);
              assert(production_false.state.pc == direct_false.state.pc);
              assert(production_false.state.pc == next_pc(state, instruction))
            },
            None() => assert(false),
          };

          state.registers[destination_index] = 0xFFFFFFFFFFFFFFFF;
          state.flags = 0b1000;
          assert(predicate_holds(instruction, state));
          match execute_SETcc(instruction, state) {
            Some(direct_true) => {
              let production_true = execute_full(instruction, state);
              assert(direct_true.fault == None());
              assert(production_true.fault == None());
              assert(not_bool(direct_true.awaiting_environment));
              assert(not_bool(production_true.awaiting_environment));
              assert(direct_true.pending.kind == CommitRegisters);
              assert(production_true.pending.kind == direct_true.pending.kind);
              assert(direct_true.state.registers[destination_index]
                     == 0x0000000000000001);
              assert(production_true.state.registers[destination_index]
                     == direct_true.state.registers[destination_index]);
              assert(production_true.state.pc == direct_true.state.pc);
              assert(production_true.state.pc == next_pc(state, instruction))
            },
            None() => assert(false),
          }
        },
        None() => assert(false),
      }
    },
    None() => assert(false),
  }

function test_divide_bounds_and_conditions() -> unit = {
  match decode_full_record([|0xC7, 0xC2, 0x29, 0x01|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000003;
      state.registers[2] = 0x11223344556677F9;
      let result = execute_full(instruction, state);
      assert(result.state.registers[2] == 0xFFFFFFFFFFFFFFFE);
      state.registers[1] = 0x00000000000000FF;
      state.registers[2] = 0x1122334455667780;
      let overflow = execute_full(instruction, state);
      assert(overflow.fault != None());
      assert(overflow.state.registers[2] == state.registers[2]);
      assert(overflow.state.pc == state.pc)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCB, 0xF0, 0x80, 0x89, 0x01|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000003;
      state.registers[2] = 0x00000000000000F9;
      let result = execute_full(instruction, state);
      assert(result.fault != None());
      assert(result.state.registers[2] == state.registers[2])
    },
    None() => assert(false),
  };
  match decode_full_record([|0xCB, 0xF0, 0x80, 0x89, 0x81|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000003;
      state.registers[2] = 0x11223344556677F9;
      state.registers[3] = 0x8877665544332200;
      let result = execute_full(instruction, state);
      assert(result.state.registers[2] == 0xFFFFFFFFFFFFFFFE);
      assert(result.state.registers[3] == 0xFFFFFFFFFFFFFFFF)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCB, 0xF0, 0x40, 0x41, 0x82|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.flags = 0b1110;
      state.registers[1] = 0x0000000000000080;
      state.registers[2] = 0x0000000000000080;
      state.registers[3] = 0x000000000000007F;
      let endpoint = execute_full(instruction, state);
      assert(endpoint.state.flags == 0b0000);
      state.registers[2] = 0x000000000000007F;
      state.registers[3] = 0x000000000000007E;
      let outside = execute_full(instruction, state);
      assert(outside.state.flags == 0b0001)
    },
    None() => assert(false),
  };

  assert(condition_holds(0, 0b0000));
  assert(not_bool(condition_holds(1, 0b1111)));
  assert(condition_holds(2, 0b1000));
  assert(condition_holds(3, 0b0000));
  assert(condition_holds(4, 0b0010));
  assert(condition_holds(5, 0b0000));
  assert(condition_holds(6, 0b0100));
  assert(condition_holds(7, 0b0000));
  assert(condition_holds(8, 0b0001));
  assert(condition_holds(9, 0b0000));
  assert(condition_holds(10, 0b1010));
  assert(condition_holds(11, 0b0000));
  assert(condition_holds(12, 0b0100));
  assert(condition_holds(13, 0b0101));
  assert(condition_holds(14, 0b1000));
  assert(condition_holds(15, 0b0000));

  test_setcc_direct_and_production()
}
