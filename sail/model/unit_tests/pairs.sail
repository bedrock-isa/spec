function assert_pair_mapping(pair_id : int) -> unit =
  if pair_id >= 8 then ()
  else {
    assert(pair_first_index(pair_id) == pair_id * 2);
    assert(unsigned(fpair_low(get_slice_int(3, pair_id, 0))) == pair_id * 2);
    assert(unsigned(fpair_high(get_slice_int(3, pair_id, 0))) == pair_id * 2 + 1);
    assert_pair_mapping(pair_id + 1)
  }

function verify_pair_stack_protocol(pair_id : int) -> unit =
  if pair_id >= 8 then ()
  else {
    let first = pair_id * 2;
    let second = first + 1;
    let first_index = unsigned(get_slice_int(4, first, 0));
    let second_index = unsigned(get_slice_int(4, second, 0));
    let first_value : bits(64) = 0x1111000000000000 | bits_from_int(first);
    let second_value : bits(64) = 0x2222000000000000 | bits_from_int(second);
    match decode_full_record([|0x10 | get_slice_int(8, pair_id, 0)|]) {
      Some(push) => {
        var state = initial_cpu(); state.sp = 0x0000000000004000;
        state.registers[first_index] = first_value;
        state.registers[second_index] = second_value;
        let range = execute_full(push, state);
        assert(range.pending.captured_first == first_value);
        assert(range.pending.captured_second == second_value);
        let store = resume_transaction(
          range, successful_response(ResponseStackRange, 0x0000000000000000, true)
        );
        assert(store.request.value == second_value);
        assert(store.request.desired == first_value);
        assert(store.request.range_start == 0x0000000000003FF0)
      },
      None() => assert(false),
    };
    match decode_full_record([|0x18 | get_slice_int(8, pair_id, 0)|]) {
      Some(pop) => {
        var state = initial_cpu(); state.sp = 0x0000000000004000;
        let range = execute_full(pop, state);
        let low = resume_transaction(
          range, successful_response(ResponseStackRange, 0x0000000000000000, true)
        );
        assert(low.request.range_start == 0x0000000000004000);
        let high = resume_transaction(
          low, successful_response(ResponseRead, second_value, true)
        );
        assert(high.request.range_start == 0x0000000000004008);
        let done = resume_transaction(
          high, successful_response(ResponseRead, first_value, true)
        );
        assert(done.state.registers[first_index] == first_value);
        assert(done.state.registers[second_index] == second_value);
        assert(done.state.sp == 0x0000000000004010)
      },
      None() => assert(false),
    };
    match decode_full_record([|0x70 | get_slice_int(8, pair_id, 0)|]) {
      Some(push) => {
        var state = initial_cpu(); state.fp_enabled = true;
        state.sp = 0x0000000000004000;
        state.floating_registers[first_index] = first_value;
        state.floating_registers[second_index] = second_value;
        let range = execute_full(push, state);
        assert(range.pending.captured_first == first_value);
        assert(range.pending.captured_second == second_value);
        let store = resume_transaction(
          range, successful_response(ResponseStackRange, 0x0000000000000000, true)
        );
        assert(store.request.value == second_value);
        assert(store.request.desired == first_value);
        assert(store.request.range_start == 0x0000000000003FF0)
      },
      None() => assert(false),
    };
    match decode_full_record([|0x78 | get_slice_int(8, pair_id, 0)|]) {
      Some(pop) => {
        var state = initial_cpu(); state.fp_enabled = true;
        state.sp = 0x0000000000004000;
        let range = execute_full(pop, state);
        let low = resume_transaction(
          range, successful_response(ResponseStackRange, 0x0000000000000000, true)
        );
        assert(low.request.range_start == 0x0000000000004000);
        let high = resume_transaction(
          low, successful_response(ResponseRead, second_value, true)
        );
        assert(high.request.range_start == 0x0000000000004008);
        let done = resume_transaction(
          high, successful_response(ResponseRead, first_value, true)
        );
        assert(done.state.floating_registers[first_index] == first_value);
        assert(done.state.floating_registers[second_index] == second_value);
        assert(done.state.sp == 0x0000000000004010)
      },
      None() => assert(false),
    };
    verify_pair_stack_protocol(pair_id + 1)
  }

