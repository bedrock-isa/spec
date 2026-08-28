function resume_system_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseCacheTranslate => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing cache translation continuation"),
      Some(instruction) => {
        {
          let granule = unsigned(previous.request.auxiliary);
          let prefetch = instruction.form.operation == Op_PREFETCH
                       | instruction.form.operation == Op_PREFETCHNT;
          let physical = response.value;
          let block_start = physical & not_vec(bits_from_int(granule - 1));
          let request = { previous.request with
            kind = if prefetch then PrefetchHint else CacheMaintenanceBlock,
            role = if prefetch then RequestRolePhysicalPrefetch
                   else RequestRolePhysicalCacheBlock,
            ordinal = previous.pending.ordinal + 1, address_translation = false,
            effective_address = physical, linear_address = physical,
            range_start = if prefetch then physical else block_start,
            range_end = if prefetch then add_bits(physical, 0x0000000000000001)
                        else add_bits(block_start, bits_from_int(granule)),
            range_length = if prefetch then 1 else granule,
            cache_policy = response.cache_policy,
            commit_point = true };
          if prefetch & response.access_class == MmioAccess then
            completed(
              previous.state, pending_after(previous),
              previous.pending.kind, [||]
            )
          else continue_with_request(
              previous, PhaseCacheMaintenance, previous.pending.ordinal + 1,
              physical, previous.pending.captured_second, request
            )
        }
      },
    },
    PhaseCacheMaintenance => completed(
      previous.state, pending_after(previous), previous.pending.kind, [||]
    ),
    PhaseFenceCompletion => completed(
      previous.state, pending_after(previous), previous.pending.kind, [||]
    ),
    PhaseTlbOperation => completed(
      previous.state, pending_after(previous), previous.pending.kind, [||]
    ),
    PhaseTranslationQuery => faulted(
      previous.state, previous.pending.operation, InvalidControlState,
      "opaque translation-query response is not accepted"
    ),
    PhasePteRead => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing PTE-walk continuation"),
      Some(instruction) => {
        let level = unsigned(previous.request.selector);
        let target_level = unsigned(previous.request.expected);
        let raw = response.value;
        let valid = pte_structurally_valid(raw, level);
        if instruction.form.operation == Op_PTQUERY & level == target_level then
          query_result(previous, raw, valid)
        else if not_bool(valid) then query_result(
          previous, 0x0000000000000000, false
        )
        else if raw[1] == bitzero then {
          if instruction.form.operation == Op_PTQUERY then
            query_result(previous, 0x0000000000000000, false)
          else {
          let physical = (raw & paging_pfn_mask(previous.state.controls[0]))
                       | (previous.request.value & paging_leaf_offset_mask(level));
          query_result(previous, physical, true)
          }
        }
        else {
          let next_level = level - 1;
          let table = raw & paging_pfn_mask(previous.state.controls[0]);
          continue_with_request(
            previous, PhasePteRead, previous.pending.ordinal + 1,
            previous.pending.captured_first, previous.pending.captured_second,
            pte_read_request(previous.state, instruction, previous.request.value,
                             table, next_level, target_level, previous.pending.ordinal + 1)
          )
        }
      },
    },
    PhaseContextSwitch => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing context-switch continuation"),
      Some(instruction) => {
        var updated = pending_after(previous);
        updated.controls[0] = previous.pending.captured_first;
        updated.controls[1] = if instruction.form.operation == Op_SWPTA
          then sail_shiftleft(previous.pending.captured_second & 0x000000000000FFFF, 16)
               | 0x0000000000000001
          else 0x0000000000000000;
        completed(previous.state, updated, CommitControl, [||])
      },
    },
    PhaseStateSave => completed(
      previous.state, pending_after(previous), CommitMemory, [||]
    ),
    PhaseStateRestoreHeader => {
      let header : bits(64) = match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      let bitmap : bits(64) = match read_le_bits(response.body_bytes, 8, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      if byte_list_length(response.body_bytes) < 16
         | header[3 .. 0] != previous.state.save_format
         | header[19 .. 11] != 0b000000000
         | header[63 .. 52] != 0x000
         | (bitmap & 0xFFFFFFFFFFFFFFFC) != 0x0000000000000000
         | (bitmap[0] == bitone & not_bool(previous.state.fp_component_present))
         | (bitmap[1] == bitone & not_bool(previous.state.vector_component_present))
      then faulted(previous.state, Op_RESTORE,
                   InvalidControlState, "invalid RESTORE header or component bitmap")
      else {
        let size = previous.state.save_area_size;
        let request = { previous.request with
          selector = 0x0000000000000001, access = AccessAddressOnly,
          range_end = add_bits(previous.request.range_start, bits_from_int(size)),
          range_length = size,
          range_wrap = size > 0
            & unsigned(add_bits(previous.request.range_start, bits_from_int(size)))
              < unsigned(previous.request.range_start)
            & add_bits(previous.request.range_start, bits_from_int(size))
              != 0x0000000000000000,
          range_end_at_modulus = size > 0
            & add_bits(previous.request.range_start, bits_from_int(size))
              == 0x0000000000000000
            & previous.request.range_start != 0x0000000000000000,
          body_length = size, commit_point = false };
        continue_with_request(
          previous, PhaseStateRestoreRange, previous.pending.ordinal + 1,
          header, bitmap, request
        )
      }
    },
    PhaseStateRestoreRange => {
      let request = { previous.request with
        selector = 0x0000000000000002, access = AccessLoad, commit_point = true,
        expected = previous.pending.captured_first,
        desired = previous.pending.captured_second,
        range_length = previous.state.save_area_size,
        body_length = previous.state.save_area_size };
      continue_with_request(
        previous, PhaseStateRestore, previous.pending.ordinal + 1,
        previous.pending.captured_first, previous.pending.captured_second, request
      )
    },
    PhaseStateRestore => {
      let image_header : bits(64) = match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      let image_bitmap : bits(64) = match read_le_bits(response.body_bytes, 8, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      if byte_list_length(response.body_bytes) < 16
         | image_header != previous.pending.captured_first
         | image_bitmap != previous.pending.captured_second then
        faulted(previous.state, Op_RESTORE, InvalidControlState,
                "RESTORE image changed after header validation")
      else restore_raw_image(previous, response.body_bytes, image_header, image_bitmap)
    },
    _ => faulted(previous.state, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
