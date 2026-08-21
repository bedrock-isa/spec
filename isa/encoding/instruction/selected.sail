enum Integer_size = SizeL | SizeQ
enum Selected_operation = Clear | Move | And | Or | Xor

struct Selected_instruction = {
  operation : Selected_operation,
  size : Integer_size,
  source : bits(4),
  destination : bits(4),
}

function decode_selected(bytes : list(bits(8))) -> option(Selected_instruction) = match bytes {
  [|byte0|] =>
    if byte0[7 .. 4] == 0x6 then
      Some(struct {
        operation = Clear,
        size = SizeQ,
        source = byte0[3 .. 0],
        destination = byte0[3 .. 0]
      })
    else None(),
  [|byte0, byte1|] => {
    let operation : option(Selected_operation) = match (byte0 & 0xFE) {
      0x80 => Some(Move),
      0x88 => Some(And),
      0x8A => Some(Or),
      0x8C => Some(Xor),
      _ => None(),
    };
    match operation {
      Some(selected) => Some(struct {
        operation = selected,
        size = if byte0[0] == bitzero then SizeL else SizeQ,
        source = byte1[7 .. 4],
        destination = byte1[3 .. 0]
      }),
      None() => None(),
    }
  },
  _ => None(),
}

type Registers = vector(16, inc, bits(64))

function binary_result(operation : Selected_operation, source : bits(64), destination : bits(64)) -> bits(64) =
  match operation {
    Move => source,
    And => source & destination,
    Or => source | destination,
    Xor => xor_vec(source, destination),
    Clear => 0x0000000000000000,
  }

function execute_selected(instruction : Selected_instruction, registers : Registers) -> Registers = {
  let source = registers[unsigned(instruction.source)];
  let destination = registers[unsigned(instruction.destination)];
  let result = binary_result(instruction.operation, source, destination);
  var updated = registers;
  updated[unsigned(instruction.destination)] = match instruction.size {
    SizeL => sail_zero_extend(result[31 .. 0], 64),
    SizeQ => result,
  };
  updated
}

function decode_and_execute(bytes : list(bits(8)), registers : Registers) -> option(Registers) =
  match decode_selected(bytes) {
    Some(instruction) => Some(execute_selected(instruction, registers)),
    None() => None(),
  }
