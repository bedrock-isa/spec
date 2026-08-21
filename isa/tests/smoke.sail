
function expect_frame(bytes : list(bits(8)), expected_class : Record_class, expected_length : int) -> unit =
  match frame_record(bytes) {
    Some(frame) => {
      assert(frame.record_class == expected_class);
      assert(frame.encoded_length == expected_length)
    },
    None() => assert(false),
  }

function expect_invalid_frame(bytes : list(bits(8))) -> unit = match frame_record(bytes) {
  Some(_) => assert(false),
  None() => (),
}

function expect_decoded(bytes : list(bits(8)), operation : Selected_operation, size : Integer_size,
                        source : bits(4), destination : bits(4)) -> unit =
  match decode_selected(bytes) {
    Some(instruction) => {
      assert(instruction.operation == operation);
      assert(instruction.size == size);
      assert(instruction.source == source);
      assert(instruction.destination == destination)
    },
    None() => assert(false),
  }

function expect_not_decoded(bytes : list(bits(8))) -> unit = match decode_selected(bytes) {
  Some(_) => assert(false),
  None() => (),
}

function expect_form(allocation : bits(64), encoding_class : Encoding_class, form_id : string) -> unit =
  match recognize_primary_form(allocation, encoding_class) {
    Some(actual) => assert(actual == form_id),
    None() => assert(false),
  }

function base_registers() -> Registers = [
  0xA5A5A5A55A5A5A5A, 0xDEADBEEFCAFEBABE, 0x02468ACE13579BDF, 0x13579BDF2468ACE0,
  0xFFFFFFFF00000000, 0x00000000FFFFFFFF, 0xFEDCBA9876543210, 0x0123456789ABCDEF,
  0x5555555555555555, 0xAAAAAAAAAAAAAAAA, 0xFFFFFFFFFFFFFFFF, 0x0000000000000000,
  0x8877665544332211, 0x0102030405060708, 0xFFEEDDCCBBAA0099, 0x1122334455667788
]

function expect_execution() -> unit = {
  let initial = base_registers();

  let clr = execute_selected(struct {
    operation = Clear, size = SizeQ, source = 0xF, destination = 0xF
  }, initial);
  assert(clr[15] == 0x0000000000000000);

  let mov_l = execute_selected(struct {
    operation = Move, size = SizeL, source = 0x0, destination = 0x1
  }, initial);
  assert(mov_l[1] == 0x0000000055667788);
  assert(mov_l[0] == initial[0]);

  let mov_q = execute_selected(struct {
    operation = Move, size = SizeQ, source = 0x0, destination = 0x1
  }, initial);
  assert(mov_q[1] == initial[0]);

  let and_l = execute_selected(struct {
    operation = And, size = SizeL, source = 0x0, destination = 0x1
  }, initial);
  assert(and_l[1] == 0x0000000011220088);

  let and_q = execute_selected(struct {
    operation = And, size = SizeQ, source = 0x0, destination = 0x1
  }, initial);
  assert(and_q[1] == 0x1122114411220088);

  let or_l = execute_selected(struct {
    operation = Or, size = SizeL, source = 0x0, destination = 0x1
  }, initial);
  assert(or_l[1] == 0x00000000FFEE7799);

  let or_q = execute_selected(struct {
    operation = Or, size = SizeQ, source = 0x6, destination = 0x7
  }, initial);
  assert(or_q[7] == 0xFFFFFFFFFFFFFFFF);

  let xor_l = execute_selected(struct {
    operation = Xor, size = SizeL, source = 0x0, destination = 0x1
  }, initial);
  assert(xor_l[1] == 0x00000000EECC7711);

  let xor_q = execute_selected(struct {
    operation = Xor, size = SizeQ, source = 0x6, destination = 0x7
  }, initial);
  assert(xor_q[7] == 0xFFFFFFFFFFFFFFFF);

  let alias = execute_selected(struct {
    operation = Xor, size = SizeQ, source = 0x8, destination = 0x8
  }, initial);
  assert(alias[8] == 0x0000000000000000);

  match decode_and_execute([|0x80, 0x01|], initial) {
    Some(updated) => assert(updated[1] == 0x0000000055667788),
    None() => assert(false),
  };
  match decode_and_execute([|0x8D, 0x88|], initial) {
    Some(updated) => assert(updated[8] == 0x0000000000000000),
    None() => assert(false),
  }
}
