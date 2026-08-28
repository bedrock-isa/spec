enum Decode_stage =
  DecodeSuccess
| DecodeFetch
| DecodeFraming
| DecodeOpcode
| DecodeConstraint
| DecodeEaDescriptor
| DecodeEaPayload
| DecodeStandalonePayload
| DecodeRecordLength
| DecodeStaticLegality
