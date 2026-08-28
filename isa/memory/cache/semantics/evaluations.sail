function first_evaluation(evaluations : list(Ea_evaluation)) -> option(Ea_evaluation) =
  match evaluations {
    [||] => None(),
    evaluation :: _ => Some(evaluation),
  }

