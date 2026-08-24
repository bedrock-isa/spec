function execute_VGATHER1(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  start_vector_memory_transaction(instruction, state)
