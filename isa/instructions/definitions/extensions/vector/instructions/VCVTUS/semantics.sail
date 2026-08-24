function execute_VCVTUS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  start_vector_fp_transaction(instruction, state)
