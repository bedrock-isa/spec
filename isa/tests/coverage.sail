function verify_representative_records(records : list(Representative_record)) -> int = match records {
  [||] => 0,
  record :: tail => match decode_full_record(legal_representative_bytes(record)) {
    None() => { assert(false); 0 },
    Some(instruction) => {
      assert(instruction.form.form_id == record.form_id);
      assert(instruction.form.mnemonic == record.mnemonic);
      assert(instruction.form.route == semantic_route(instruction.form.operation));
      1 + verify_representative_records(tail)
    },
  },
}

function verify_no_generic_external_fallback_one(record : Representative_record) -> int =
  match decode_full_record(legal_representative_bytes(record)) {
    None() => { assert(false); 0 },
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true; state.status = 0x0000000000000010;
      state.fp_enabled = true; state.fptrans_enabled = true;
      let result = execute_full(instruction, state);
      assert(result.request.kind != ExternalIntegerRequest);
      1
    },
  }

function verify_no_generic_external_fallback(records : list(Representative_record)) -> int =
  match records {
    [||] => 0,
    record :: tail => {
      let verified = verify_no_generic_external_fallback_one(record);
      verified + verify_no_generic_external_fallback(tail)
    },
  }

function verify_fp_first_phase_one(record : Representative_record) -> int =
  match decode_full_record(legal_representative_bytes(record)) {
    None() => { assert(false); 0 },
    Some(instruction) => {
      let fp_form = instruction.form.route == RouteFpu
                  | instruction.form.route == RouteFpuTranscendental;
      if not_bool(fp_form) then 0
      else {
        var state = initial_cpu();
        state.fp_enabled = true; state.fptrans_enabled = true;
        let result = execute_full(instruction, state);
        assert(result.fault == None());
        assert(result.request.kind != ExternalIntegerRequest);
        if instruction.form.operation == Op_FPUSHP
           | instruction.form.operation == Op_FPOPP then
          assert(result.pending.phase == PhaseStackRange)
        else if instruction.form.instruction_set == FpuTranscendentalSet then
          assert(result.pending.phase == PhaseFpContractQuery)
        else if result.awaiting_environment then
          assert(result.pending.phase == PhaseFpSourceRead
                 | result.pending.phase == PhaseFpDestinationProbe
                 | result.pending.phase == PhaseFpCompute)
        else assert(result.pending.phase == ContinuationNone);
        1
      }
    },
  }

function verify_fp_first_phase(records : list(Representative_record)) -> int = match records {
  [||] => 0,
  record :: tail => {
    let verified = verify_fp_first_phase_one(record);
    verified + verify_fp_first_phase(tail)
  },
}

function non_fp_operation(operation : Semantic_operation) -> bool =
  semantic_route(operation) != RouteFpu
  & semantic_route(operation) != RouteFpuTranscendental

function count_non_fp_operations(operations : list(Semantic_operation)) -> int = match operations {
  [||] => 0,
  operation :: tail => (if non_fp_operation(operation) then 1 else 0)
                       + count_non_fp_operations(tail),
}

function non_fp_form(instruction : Decoded_instruction) -> bool =
  instruction.form.instruction_set == BaseSet
  | instruction.form.operation == Op_RDFFLAGS
  | instruction.form.operation == Op_WRFFLAGS
  | instruction.form.operation == Op_RDFSTATUS
  | instruction.form.operation == Op_WRFSTATUS

function verify_non_fp_routes_chunk(records : list(Representative_record), state : Cpu_state,
                                    budget : int)
  -> (int, list(Representative_record)) =
  if budget == 0 then (0, records)
  else match records {
    [||] => (0, [||]),
    record :: tail => match decode_full_record(legal_representative_bytes(record)) {
      None() => { assert(false); (0, [||]) },
      Some(instruction) => {
        let selected = non_fp_form(instruction);
        if selected then {
          let result = execute_full(instruction, state);
          if result.awaiting_environment then {
            assert(result.request.kind != NoPrimitiveRequest);
            assert(result.pending.phase != ContinuationNone);
            assert(result.pending.instruction != None());
            let wrong_kind = if result.pending.phase == PhaseResetSerialize
                             then ResponseRead else ResponseResetSerialize;
            let rejected = resume_transaction(
              result, successful_response(wrong_kind, 0x0000000000000000, true)
            );
            assert(rejected.state == state);
            assert(rejected.fault != None())
          }
          else match result.fault {
            Some(fault) => if instruction.form.operation == Op_ILLEGAL then ()
                           else assert(fault.kind != IllegalInstruction),
            None() => (),
          };
        } else ();
        let (chunk_count, remaining) = verify_non_fp_routes_chunk(
          tail, state, budget - 1
        );
        ((if selected then 1 else 0) + chunk_count, remaining)
      },
    },
  }

function verify_non_fp_routes(records : list(Representative_record), state : Cpu_state) -> int =
  match records {
    [||] => 0,
    _ => {
      let (chunk_count, remaining) = verify_non_fp_routes_chunk(records, state, 16);
      chunk_count + verify_non_fp_routes(remaining, state)
    },
  }

function local_operation_required(operation : Semantic_operation) -> bool = match operation {
  Op_ABS => true, Op_ADC => true, Op_ADD => true, Op_AND => true,
  Op_BCHG => true, Op_BCLR => true, Op_BSET => true, Op_BTEST => true,
  Op_BNDSII => true, Op_BNDSIX => true, Op_BNDSXI => true, Op_BNDSXX => true,
  Op_BNDUII => true, Op_BNDUIX => true, Op_BNDUXI => true, Op_BNDUXX => true,
  Op_CLMUL => true, Op_CLMULH => true, Op_CLR => true, Op_CLS => true,
  Op_CLZ => true, Op_CMP => true, Op_CTS => true, Op_CTZ => true,
  Op_DEC => true, Op_DECF => true, Op_DIVMODS => true, Op_DIVMODU => true,
  Op_DIVS => true, Op_DIVU => true, Op_EXTRACT => true,
  Op_EXTSL => true, Op_EXTSQ => true, Op_EXTSW => true,
  Op_EXTZL => true, Op_EXTZQ => true, Op_EXTZW => true,
  Op_INC => true, Op_INCF => true, Op_MAXS => true, Op_MAXU => true,
  Op_MINS => true, Op_MINU => true, Op_MODS => true, Op_MODU => true,
  Op_MOV => true, Op_MOVcc => true, Op_MUL => true, Op_MULHS => true,
  Op_MULHSU => true, Op_MULHU => true, Op_NEG => true, Op_NOT => true,
  Op_OR => true, Op_PARITY => true, Op_POPCNT => true, Op_REVBYTE => true,
  Op_ROL => true, Op_ROR => true, Op_SAR => true, Op_SBB => true,
  Op_SET => true, Op_SETcc => true, Op_SHL => true, Op_SHR => true,
  Op_SUB => true, Op_TEST => true, Op_XCHG => true, Op_XOR => true,
  Op_SETF => true, Op_RDCR => true,
  Op_RDFLAGS => true, Op_WRFLAGS => true, Op_RDSTATUS => true, Op_WRSTATUS => true,
  Op_RDSEG => true, Op_WRSEG => true,
  Op_RDFFLAGS => true, Op_WRFFLAGS => true,
  Op_RDFSTATUS => true, Op_WRFSTATUS => true,
  Op_NOP => true, Op_WAIT => true, Op_YIELD => true,
  Op_TRACE => true, Op_HALT => true, Op_ILLEGAL => true,
  _ => false,
}

function verify_local_representatives(records : list(Representative_record), state : Cpu_state)
  -> int = match records {
  [||] => 0,
  record :: tail => match decode_full_record(legal_representative_bytes(record)) {
    None() => { assert(false); 0 },
    Some(instruction) => {
      if local_operation_required(instruction.form.operation)
         & operands_local(state, instruction.operands) then {
        let result = execute_full(instruction, state);
        assert(not_bool(result.awaiting_environment));
        match result.fault {
          Some(fault) => if instruction.form.operation == Op_ILLEGAL then ()
            else if fault.kind == IllegalInstruction then assert(false)
            else (),
          None() => (),
        }
      } else ();
      1 + verify_local_representatives(tail, state)
    },
  },
}
