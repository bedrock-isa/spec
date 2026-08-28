#include "bedrock_core_abi.h"

struct bedrock_core {
  struct zCpu_state state;
  struct zExecution_result pending;
  bool has_pending;
  bedrock_core_fault fault;
  bedrock_core_request request;
  bedrock_core_status last_status;
};

static size_t bedrock_core_instance_count = 0;

static void bedrock_core_clear_observation(bedrock_core *core) {
  memset(&core->fault, 0, sizeof(core->fault));
  memset(&core->request, 0, sizeof(core->request));
  core->last_status = BEDROCK_CORE_OK;
}

static zz5listz8z5bvz9 bedrock_core_byte_list(
    const uint8_t *bytes, size_t length) {
  zz5listz8z5bvz9 result;
  CREATE(zz5listz8z5bvz9)(&result);
  for (size_t index = length; index > 0; --index) {
    lbits byte;
    CREATE(lbits)(&byte);
    CONVERT_OF(lbits, fbits)(&byte, bytes[index - 1], UINT64_C(8), true);
    zconsz3z5bv(&result, byte, result);
    KILL(lbits)(&byte);
  }
  return result;
}

static size_t bedrock_core_byte_list_length(zz5listz8z5bvz9 bytes) {
  size_t length = 0;
  for (zz5listz8z5bvz9 cursor = bytes; cursor != NULL; cursor = cursor->tl)
    length += 1;
  return length;
}

static bool bedrock_core_byte_list_to_array(
    zz5listz8z5bvz9 bytes, uint8_t *output, size_t length) {
  size_t index = 0;
  for (zz5listz8z5bvz9 cursor = bytes; cursor != NULL; cursor = cursor->tl) {
    if (index >= length) return false;
    output[index++] =
        (uint8_t)CONVERT_OF(fbits, lbits)(cursor->hd, true);
  }
  return index == length;
}

static bool bedrock_core_state_shape_valid(const struct zCpu_state *state) {
  if (state->zregisters.len != BEDROCK_CORE_REGISTER_COUNT
      || state->zfloating_registers.len != BEDROCK_CORE_FLOATING_REGISTER_COUNT
      || state->zsegments.len != BEDROCK_CORE_SEGMENT_COUNT
      || state->zcontrols.len != BEDROCK_CORE_CONTROL_COUNT
      || state->zvector_registers.len != BEDROCK_CORE_VECTOR_REGISTER_COUNT
      || state->zpredicate_registers.len != BEDROCK_CORE_PREDICATE_REGISTER_COUNT
      || mpz_get_si(state->zvector_length_bytes)
             != BEDROCK_CORE_VECTOR_LENGTH_BYTES)
    return false;
  for (size_t index = 0; index < BEDROCK_CORE_VECTOR_REGISTER_COUNT; ++index)
    if (bedrock_core_byte_list_length(state->zvector_registers.data[index])
        != BEDROCK_CORE_VECTOR_LENGTH_BYTES)
      return false;
  for (size_t index = 0; index < BEDROCK_CORE_PREDICATE_REGISTER_COUNT; ++index)
    if (bedrock_core_byte_list_length(state->zpredicate_registers.data[index])
        != BEDROCK_CORE_PREDICATE_LENGTH_BYTES)
      return false;
  return true;
}

static void bedrock_core_replace_byte_list(
    zz5listz8z5bvz9 *destination, const uint8_t *bytes, size_t length) {
  zz5listz8z5bvz9 replacement = bedrock_core_byte_list(bytes, length);
  COPY(zz5listz8z5bvz9)(destination, replacement);
  KILL(zz5listz8z5bvz9)(&replacement);
}

static void bedrock_core_discard_pending(bedrock_core *core) {
  RECREATE(zExecution_result)(&core->pending);
  core->has_pending = false;
}

static bedrock_core_status bedrock_core_accept_execution(
    bedrock_core *core, const struct zExecution_result *execution) {
  bedrock_core_clear_observation(core);
  COPY(zCpu_state)(&core->state, execution->zstate);

  if (execution->zfault.kind == Kind_zSomezIRExecution_faultzK) {
    struct zExecution_fault *fault =
        (struct zExecution_fault *)&execution->zfault.variants.zSomezIRExecution_faultzK;
    bedrock_core_discard_pending(core);
    core->fault.kind = fault->zkind;
    core->fault.operation = fault->zoperation;
    core->fault.error_code = fault->zerror_code;
    core->fault.bus_error = fault->zbus_error ? 1 : 0;
    core->last_status = BEDROCK_CORE_FAULT;
  } else if (execution->zawaiting_environment) {
    struct zPrimitive_request *request =
        (struct zPrimitive_request *)&execution->zrequest;
    RECREATE(zExecution_result)(&core->pending);
    COPY(zExecution_result)(&core->pending, *execution);
    core->has_pending = true;
    core->request.kind = request->zkind;
    core->request.operation = execution->zpending.zoperation;
    core->request.form_id = zForm_invalid;
    if (execution->zpending.zinstruction.kind == Kind_zSomezIRDecoded_instructionzK)
      core->request.form_id = execution->zpending.zinstruction.variants
                                  .zSomezIRDecoded_instructionzK.zform.zform_id;
    core->request.access = request->zaccess;
    core->request.role = request->zrole;
    core->request.domain = request->zdomain;
    core->request.segment = mpz_get_si(request->zsegment);
    core->request.segment_image = request->zsegment_image;
    core->request.width = mpz_get_si(request->zwidth);
    core->request.ordinal = mpz_get_si(request->zordinal);
    core->request.range_length = mpz_get_si(request->zrange_length);
    core->request.range_wrap = request->zrange_wrap ? 1 : 0;
    core->request.range_end_at_modulus = request->zrange_end_at_modulus ? 1 : 0;
    core->request.effective_address = request->zeffective_address;
    core->request.linear_address = request->zlinear_address;
    core->request.value = request->zvalue;
    core->request.desired = request->zdesired;
    core->request.expected = request->zexpected;
    core->request.range_start = request->zrange_start;
    core->request.range_end = request->zrange_end;
    core->request.address_translation = request->zaddress_translation ? 1 : 0;
    core->request.commit_point = request->zcommit_point ? 1 : 0;
    core->request.memory_order = mpz_get_si(request->zmemory_order);
    core->request.cache_policy = mpz_get_si(request->zcache_policy);
    core->request.suppress_fault = request->zsuppress_fault ? 1 : 0;
    core->request.selector = request->zselector;
    core->request.auxiliary = request->zauxiliary;
    core->request.body_length = mpz_get_si(request->zbody_length);
    core->request.payload_length =
        bedrock_core_byte_list_length(request->zpayload_bytes);
    core->last_status = BEDROCK_CORE_NEEDS_ENVIRONMENT;
  } else {
    bedrock_core_discard_pending(core);
  }
  return core->last_status;
}

uint32_t bedrock_core_abi_version(void) {
  return BEDROCK_CORE_ABI_VERSION;
}

size_t bedrock_core_state_size(void) {
  return sizeof(bedrock_core_state);
}

bedrock_core *bedrock_core_create(void) {
  if (bedrock_core_instance_count == 0) model_init();
  bedrock_core *core = malloc(sizeof(*core));
  if (core == NULL) {
    if (bedrock_core_instance_count == 0) model_fini();
    return NULL;
  }
  CREATE(zCpu_state)(&core->state);
  CREATE(zExecution_result)(&core->pending);
  zinitial_cpu(&core->state, UNIT);
  core->has_pending = false;
  bedrock_core_clear_observation(core);
  bedrock_core_instance_count += 1;
  return core;
}

void bedrock_core_destroy(bedrock_core *core) {
  if (core == NULL) return;
  KILL(zExecution_result)(&core->pending);
  KILL(zCpu_state)(&core->state);
  free(core);
  bedrock_core_instance_count -= 1;
  if (bedrock_core_instance_count == 0) model_fini();
}

bedrock_core_status bedrock_core_reset(bedrock_core *core) {
  if (core == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  struct zCpu_state reset;
  CREATE(zCpu_state)(&reset);
  zplatform_reset(&reset, core->state);
  COPY(zCpu_state)(&core->state, reset);
  KILL(zCpu_state)(&reset);
  bedrock_core_discard_pending(core);
  bedrock_core_clear_observation(core);
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_get_pc(const bedrock_core *core, uint64_t *value) {
  if (core == NULL || value == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  *value = core->state.zpc;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_set_pc(bedrock_core *core, uint64_t value) {
  if (core == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (core->has_pending) return BEDROCK_CORE_BAD_STATE;
  core->state.zpc = value;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_get_sp(const bedrock_core *core, uint64_t *value) {
  if (core == NULL || value == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  *value = core->state.zsp;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_set_sp(bedrock_core *core, uint64_t value) {
  if (core == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (core->has_pending) return BEDROCK_CORE_BAD_STATE;
  core->state.zsp = value;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_get_register(
    const bedrock_core *core, uint32_t index, uint64_t *value) {
  if (core == NULL || value == NULL || index >= core->state.zregisters.len)
    return BEDROCK_CORE_BAD_ARGUMENT;
  *value = core->state.zregisters.data[index];
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_set_register(
    bedrock_core *core, uint32_t index, uint64_t value) {
  if (core == NULL || index >= core->state.zregisters.len)
    return BEDROCK_CORE_BAD_ARGUMENT;
  if (core->has_pending) return BEDROCK_CORE_BAD_STATE;
  core->state.zregisters.data[index] = value;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_get_status(
    const bedrock_core *core, uint64_t *value) {
  if (core == NULL || value == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  *value = core->state.zstatus;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_get_control(
    const bedrock_core *core, uint32_t index, uint64_t *value) {
  if (core == NULL || value == NULL || index >= core->state.zcontrols.len)
    return BEDROCK_CORE_BAD_ARGUMENT;
  *value = core->state.zcontrols.data[index];
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_is_supervisor(
    const bedrock_core *core, uint8_t *value) {
  if (core == NULL || value == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  *value = core->state.zsupervisor ? 1 : 0;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_get_state(
    const bedrock_core *core, bedrock_core_state *state) {
  if (core == NULL || state == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (!bedrock_core_state_shape_valid(&core->state)) return BEDROCK_CORE_BAD_STATE;
  memset(state, 0, sizeof(*state));
  memcpy(state->registers, core->state.zregisters.data,
         sizeof(state->registers));
  memcpy(state->floating_registers, core->state.zfloating_registers.data,
         sizeof(state->floating_registers));
  memcpy(state->segments, core->state.zsegments.data, sizeof(state->segments));
  memcpy(state->controls, core->state.zcontrols.data, sizeof(state->controls));
  for (size_t index = 0; index < BEDROCK_CORE_VECTOR_REGISTER_COUNT; ++index)
    if (!bedrock_core_byte_list_to_array(
            core->state.zvector_registers.data[index],
            state->vector_registers[index], BEDROCK_CORE_VECTOR_LENGTH_BYTES))
      return BEDROCK_CORE_BAD_STATE;
  for (size_t index = 0; index < BEDROCK_CORE_PREDICATE_REGISTER_COUNT; ++index)
    if (!bedrock_core_byte_list_to_array(
            core->state.zpredicate_registers.data[index],
            state->predicate_registers[index],
            BEDROCK_CORE_PREDICATE_LENGTH_BYTES))
      return BEDROCK_CORE_BAD_STATE;
  state->sp = core->state.zsp;
  state->pc = core->state.zpc;
  state->flags = core->state.zflags;
  state->status = core->state.zstatus;
  state->fstatus = core->state.zfstatus;
  state->fflags = core->state.zfflags;
  state->current_dfa = core->state.zcurrent_dfa ? 1 : 0;
  state->supervisor = core->state.zsupervisor ? 1 : 0;
  state->halted = core->state.zhalted ? 1 : 0;
  state->run_state = core->state.zrun_state;
  state->fp_enabled = core->state.zfp_enabled ? 1 : 0;
  state->fptrans_enabled = core->state.zfptrans_enabled ? 1 : 0;
  state->vector_enabled = core->state.zvector_enabled ? 1 : 0;
  state->cache_maintenance_granule = core->state.zcache_maintenance_granule;
  state->fp_component_alignment = core->state.zfp_component_alignment;
  state->fp_component_bitmap_bit = core->state.zfp_component_bitmap_bit;
  state->fp_component_id = core->state.zfp_component_id;
  state->fp_component_init_policy = core->state.zfp_component_init_policy;
  state->fp_component_modified = core->state.zfp_component_modified ? 1 : 0;
  state->fp_component_offset = mpz_get_si(core->state.zfp_component_offset);
  state->fp_component_present = core->state.zfp_component_present ? 1 : 0;
  state->fp_component_size = mpz_get_si(core->state.zfp_component_sizze);
  state->vector_component_alignment = core->state.zvector_component_alignment;
  state->vector_component_bitmap_bit = core->state.zvector_component_bitmap_bit;
  state->vector_component_id = core->state.zvector_component_id;
  state->vector_component_init_policy = core->state.zvector_component_init_policy;
  state->vector_component_modified = core->state.zvector_component_modified ? 1 : 0;
  state->vector_component_offset = mpz_get_si(core->state.zvector_component_offset);
  state->vector_component_present = core->state.zvector_component_present ? 1 : 0;
  state->vector_component_size = mpz_get_si(core->state.zvector_component_sizze);
  state->vector_length_bytes = mpz_get_si(core->state.zvector_length_bytes);
  state->machine_check_error_code = core->state.zmachine_check_error_code;
  state->machine_check_event_aux = core->state.zmachine_check_event_aux;
  state->machine_check_fault_ea = core->state.zmachine_check_fault_ea;
  state->machine_check_fault_linear = core->state.zmachine_check_fault_linear;
  state->machine_check_payload = core->state.zmachine_check_payload;
  state->machine_check_pending = core->state.zmachine_check_pending ? 1 : 0;
  state->nmi_latched_source = core->state.znmi_latched_source;
  state->nmi_relatched = core->state.znmi_relatched ? 1 : 0;
  state->nmi_relatched_source = core->state.znmi_relatched_source;
  state->repeat_active = core->state.zrepeat_state.zactive ? 1 : 0;
  state->repeat_body_start = core->state.zrepeat_state.zbody_start;
  state->repeat_condition = core->state.zrepeat_state.zcondition;
  state->repeat_counter = core->state.zrepeat_state.zcounter;
  state->repeat_prefix_start = core->state.zrepeat_state.zprefix_start;
  state->repeat_remaining = core->state.zrepeat_state.zremaining;
  state->repeat_fixed_body_length =
      bedrock_core_byte_list_length(core->state.zrepeat_state.zfixed_body);
  if (state->repeat_fixed_body_length > BEDROCK_CORE_MAX_INSTRUCTION_BYTES
      || !bedrock_core_byte_list_to_array(
          core->state.zrepeat_state.zfixed_body, state->repeat_fixed_body,
          state->repeat_fixed_body_length))
    return BEDROCK_CORE_BAD_STATE;
  state->save_area_size = mpz_get_si(core->state.zsave_area_sizze);
  state->save_bitmap_words = core->state.zsave_bitmap_words;
  state->save_fixed_size = mpz_get_si(core->state.zsave_fixed_sizze);
  state->save_format = core->state.zsave_format;
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_set_state(
    bedrock_core *core, const bedrock_core_state *state) {
  if (core == NULL || state == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (core->has_pending) return BEDROCK_CORE_BAD_STATE;
  if (!bedrock_core_state_shape_valid(&core->state)
      || state->run_state < zRunning || state->run_state > zShutdown
      || state->vector_length_bytes != BEDROCK_CORE_VECTOR_LENGTH_BYTES
      || state->repeat_fixed_body_length > BEDROCK_CORE_MAX_INSTRUCTION_BYTES)
    return BEDROCK_CORE_BAD_ARGUMENT;
  memcpy(core->state.zregisters.data, state->registers,
         sizeof(state->registers));
  memcpy(core->state.zfloating_registers.data, state->floating_registers,
         sizeof(state->floating_registers));
  memcpy(core->state.zsegments.data, state->segments, sizeof(state->segments));
  memcpy(core->state.zcontrols.data, state->controls, sizeof(state->controls));
  for (size_t index = 0; index < BEDROCK_CORE_VECTOR_REGISTER_COUNT; ++index)
    bedrock_core_replace_byte_list(&core->state.zvector_registers.data[index],
                                   state->vector_registers[index],
                                   BEDROCK_CORE_VECTOR_LENGTH_BYTES);
  for (size_t index = 0; index < BEDROCK_CORE_PREDICATE_REGISTER_COUNT; ++index)
    bedrock_core_replace_byte_list(&core->state.zpredicate_registers.data[index],
                                   state->predicate_registers[index],
                                   BEDROCK_CORE_PREDICATE_LENGTH_BYTES);
  core->state.zsp = state->sp;
  core->state.zpc = state->pc;
  core->state.zflags = state->flags;
  core->state.zstatus = state->status;
  core->state.zfstatus = state->fstatus;
  core->state.zfflags = state->fflags;
  core->state.zcurrent_dfa = state->current_dfa != 0;
  core->state.zsupervisor = state->supervisor != 0;
  core->state.zhalted = state->halted != 0;
  core->state.zrun_state = (enum zRun_state)state->run_state;
  core->state.zfp_enabled = state->fp_enabled != 0;
  core->state.zfptrans_enabled = state->fptrans_enabled != 0;
  core->state.zvector_enabled = state->vector_enabled != 0;
  core->state.zcache_maintenance_granule = state->cache_maintenance_granule;
  core->state.zfp_component_alignment = state->fp_component_alignment;
  core->state.zfp_component_bitmap_bit = state->fp_component_bitmap_bit;
  core->state.zfp_component_id = state->fp_component_id;
  core->state.zfp_component_init_policy = state->fp_component_init_policy;
  core->state.zfp_component_modified = state->fp_component_modified != 0;
  mpz_set_si(core->state.zfp_component_offset, state->fp_component_offset);
  core->state.zfp_component_present = state->fp_component_present != 0;
  mpz_set_si(core->state.zfp_component_sizze, state->fp_component_size);
  core->state.zvector_component_alignment = state->vector_component_alignment;
  core->state.zvector_component_bitmap_bit = state->vector_component_bitmap_bit;
  core->state.zvector_component_id = state->vector_component_id;
  core->state.zvector_component_init_policy = state->vector_component_init_policy;
  core->state.zvector_component_modified = state->vector_component_modified != 0;
  mpz_set_si(core->state.zvector_component_offset, state->vector_component_offset);
  core->state.zvector_component_present = state->vector_component_present != 0;
  mpz_set_si(core->state.zvector_component_sizze, state->vector_component_size);
  mpz_set_si(core->state.zvector_length_bytes, state->vector_length_bytes);
  core->state.zmachine_check_error_code = state->machine_check_error_code;
  core->state.zmachine_check_event_aux = state->machine_check_event_aux;
  core->state.zmachine_check_fault_ea = state->machine_check_fault_ea;
  core->state.zmachine_check_fault_linear = state->machine_check_fault_linear;
  core->state.zmachine_check_payload = state->machine_check_payload;
  core->state.zmachine_check_pending = state->machine_check_pending != 0;
  core->state.znmi_latched_source = state->nmi_latched_source;
  core->state.znmi_relatched = state->nmi_relatched != 0;
  core->state.znmi_relatched_source = state->nmi_relatched_source;
  core->state.zrepeat_state.zactive = state->repeat_active != 0;
  core->state.zrepeat_state.zbody_start = state->repeat_body_start;
  core->state.zrepeat_state.zcondition = state->repeat_condition;
  core->state.zrepeat_state.zcounter = state->repeat_counter;
  core->state.zrepeat_state.zprefix_start = state->repeat_prefix_start;
  core->state.zrepeat_state.zremaining = state->repeat_remaining;
  bedrock_core_replace_byte_list(&core->state.zrepeat_state.zfixed_body,
                                 state->repeat_fixed_body,
                                 state->repeat_fixed_body_length);
  mpz_set_si(core->state.zsave_area_sizze, state->save_area_size);
  core->state.zsave_bitmap_words = state->save_bitmap_words;
  mpz_set_si(core->state.zsave_fixed_sizze, state->save_fixed_size);
  core->state.zsave_format = state->save_format;
  bedrock_core_clear_observation(core);
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_execute(
    bedrock_core *core, const uint8_t *bytes, size_t length) {
  if (core == NULL || bytes == NULL || length == 0
      || length > BEDROCK_CORE_MAX_INSTRUCTION_BYTES)
    return BEDROCK_CORE_BAD_ARGUMENT;
  if (core->has_pending) return BEDROCK_CORE_BAD_STATE;

  zz5listz8z5bvz9 input = bedrock_core_byte_list(bytes, length);
  struct zoptionzIRExecution_resultzK result;
  CREATE(zoptionzIRExecution_resultzK)(&result);
  zdecode_and_execute_full(&result, input, core->state);
  KILL(zz5listz8z5bvz9)(&input);
  if (result.kind == Kind_zNonezIRExecution_resultzK) {
    bedrock_core_clear_observation(core);
    core->last_status = BEDROCK_CORE_INVALID_INSTRUCTION;
  } else {
    struct zExecution_result *execution =
        &result.variants.zSomezIRExecution_resultzK;
    bedrock_core_accept_execution(core, execution);
  }

  KILL(zoptionzIRExecution_resultzK)(&result);
  return core->last_status;
}

bedrock_core_status bedrock_core_last_fault(
    const bedrock_core *core, bedrock_core_fault *fault) {
  if (core == NULL || fault == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (core->last_status != BEDROCK_CORE_FAULT) return core->last_status;
  *fault = core->fault;
  return BEDROCK_CORE_FAULT;
}

bedrock_core_status bedrock_core_last_request(
    const bedrock_core *core, bedrock_core_request *request) {
  if (core == NULL || request == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (core->last_status != BEDROCK_CORE_NEEDS_ENVIRONMENT)
    return core->last_status;
  *request = core->request;
  return BEDROCK_CORE_NEEDS_ENVIRONMENT;
}

bedrock_core_status bedrock_core_request_payload(
    const bedrock_core *core, uint8_t *buffer, size_t capacity, size_t *length) {
  if (core == NULL || length == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (!core->has_pending || core->last_status != BEDROCK_CORE_NEEDS_ENVIRONMENT)
    return core->last_status == BEDROCK_CORE_OK ? BEDROCK_CORE_BAD_STATE
                                                : core->last_status;
  size_t required = core->request.payload_length;
  *length = required;
  if (buffer == NULL && capacity == 0)
    return BEDROCK_CORE_NEEDS_ENVIRONMENT;
  if (required > capacity || (required != 0 && buffer == NULL))
    return BEDROCK_CORE_BAD_ARGUMENT;
  size_t index = 0;
  for (zz5listz8z5bvz9 cursor = core->pending.zrequest.zpayload_bytes;
       cursor != NULL; cursor = cursor->tl)
    buffer[index++] =
        (uint8_t)CONVERT_OF(fbits, lbits)(cursor->hd, true);
  return BEDROCK_CORE_NEEDS_ENVIRONMENT;
}

bedrock_core_status bedrock_core_cancel(bedrock_core *core) {
  if (core == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (!core->has_pending) return BEDROCK_CORE_BAD_STATE;
  bedrock_core_discard_pending(core);
  bedrock_core_clear_observation(core);
  return BEDROCK_CORE_OK;
}

bedrock_core_status bedrock_core_resume(
    bedrock_core *core, const bedrock_core_response *response) {
  if (core == NULL || response == NULL) return BEDROCK_CORE_BAD_ARGUMENT;
  if (!core->has_pending || core->last_status != BEDROCK_CORE_NEEDS_ENVIRONMENT)
    return BEDROCK_CORE_BAD_STATE;
  if (response->body_length != 0 && response->body_bytes == NULL)
    return BEDROCK_CORE_BAD_ARGUMENT;

  struct zTransaction_response transaction;
  CREATE(zTransaction_response)(&transaction);
  transaction.zkind = (enum zTransaction_response_kind)response->kind;
  transaction.zsuccess = response->success != 0;
  transaction.zfault_kind = (enum zFault_kind)response->fault_kind;
  mpz_set_si(transaction.zfault_cause, response->fault_cause);
  COPY(sail_string)(&transaction.zdetail,
                    response->detail == NULL ? "" : response->detail);
  transaction.zvalue = response->value;
  transaction.zsecondary_value = response->secondary_value;
  transaction.zflags = response->flags;
  transaction.zwrite_flags = response->write_flags != 0;
  transaction.zgenerated_fflags = response->generated_fflags;
  transaction.zbounds_passed = response->bounds_passed != 0;
  mpz_set_si(transaction.zcache_policy, response->cache_policy);
  transaction.zaccess_class = (enum zMemory_access_class)response->access_class;
  transaction.zphysical_class =
      (enum zPhysical_memory_class)response->physical_class;
  transaction.zatomic_store_happened = response->atomic_store_happened != 0;
  transaction.zbody_bytes =
      bedrock_core_byte_list(response->body_bytes, response->body_length);
  transaction.zknown = response->known != 0;
  transaction.zpresent = response->present != 0;
  struct zExecution_result result;
  CREATE(zExecution_result)(&result);
  zresume_transaction(&result, core->pending, transaction);
  bedrock_core_status status = bedrock_core_accept_execution(core, &result);
  KILL(zExecution_result)(&result);
  KILL(zTransaction_response)(&transaction);
  return status;
}
