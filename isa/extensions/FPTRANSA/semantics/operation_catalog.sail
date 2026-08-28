function clause fp_semantics(
  operation if semantic_route(operation) != RouteFpu
            & semantic_route(operation) != RouteFpuTranscendental
) = None()
