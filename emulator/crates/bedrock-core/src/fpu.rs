pub mod base_arithmetic;
pub mod base_convert_compare;
pub mod effect;
pub mod env;
pub mod format;
pub mod trans;

use effect::{FpEffect, FpRequest};
use trans::contracts::TransOperation;

/// Routes one FPTRANSA request to its pure numerical domain evaluator.
pub fn execute_trans(operation: TransOperation, request: FpRequest<'_>) -> FpEffect {
    match operation {
        TransOperation::Sine
        | TransOperation::Cosine
        | TransOperation::Tangent
        | TransOperation::SineCosine
        | TransOperation::ArcSine
        | TransOperation::ArcCosine
        | TransOperation::ArcTangent => trans::circular::execute(operation, request),
        TransOperation::HyperbolicSine
        | TransOperation::HyperbolicCosine
        | TransOperation::HyperbolicTangent
        | TransOperation::HyperbolicArcTangent => trans::hyperbolic::execute(operation, request),
        TransOperation::Exponential
        | TransOperation::ExponentialMinusOne
        | TransOperation::ExponentialBaseTwo
        | TransOperation::ExponentialBaseTen
        | TransOperation::NaturalLogarithm
        | TransOperation::NaturalLogarithmPlusOne
        | TransOperation::LogarithmBaseTwo
        | TransOperation::LogarithmBaseTen => trans::exp_log::execute(operation, request),
    }
}

#[cfg(test)]
mod tests {
    use super::{execute_trans, trans};
    use crate::fpu::{
        effect::FpRequest, env::FpStatus, format::FpFormat, trans::contracts::TransOperation,
    };

    #[test]
    fn facade_routes_all_seven_four_and_eight_operations() {
        let operand = [0_u64];
        let request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode(0).unwrap(),
            operands: &operand,
        };
        let circular = [
            TransOperation::Sine,
            TransOperation::Cosine,
            TransOperation::Tangent,
            TransOperation::SineCosine,
            TransOperation::ArcSine,
            TransOperation::ArcCosine,
            TransOperation::ArcTangent,
        ];
        let hyperbolic = [
            TransOperation::HyperbolicSine,
            TransOperation::HyperbolicCosine,
            TransOperation::HyperbolicTangent,
            TransOperation::HyperbolicArcTangent,
        ];
        let exp_log = [
            TransOperation::Exponential,
            TransOperation::ExponentialMinusOne,
            TransOperation::ExponentialBaseTwo,
            TransOperation::ExponentialBaseTen,
            TransOperation::NaturalLogarithm,
            TransOperation::NaturalLogarithmPlusOne,
            TransOperation::LogarithmBaseTwo,
            TransOperation::LogarithmBaseTen,
        ];

        for operation in circular {
            assert_eq!(
                execute_trans(operation, request),
                trans::circular::execute(operation, request)
            );
        }
        for operation in hyperbolic {
            assert_eq!(
                execute_trans(operation, request),
                trans::hyperbolic::execute(operation, request)
            );
        }
        for operation in exp_log {
            assert_eq!(
                execute_trans(operation, request),
                trans::exp_log::execute(operation, request)
            );
        }
    }
}
