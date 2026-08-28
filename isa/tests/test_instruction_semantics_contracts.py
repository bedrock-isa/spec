from pathlib import Path
import re
import unittest


class InstructionSemanticsContractTest(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[1]
    DEFINITIONS = ROOT / "instructions" / "definitions"

    def register_result_extension(self, mnemonic: str) -> str:
        source = (self.DEFINITIONS / mnemonic / "semantics.sail").read_text()
        match = re.search(
            rf"register_result_extension\(Op_{re.escape(mnemonic)}\) = (\w+)",
            source,
        )
        self.assertIsNotNone(match, mnemonic)
        return match.group(1)

    def test_signed_scalar_results_are_sign_extended(self) -> None:
        signed_results = {
            "ABS",
            "DIVS",
            "MODS",
            "DIVMODS",
            "MINS",
            "MAXS",
            "SAR",
            "EXTSW",
            "EXTSL",
            "EXTSQ",
        }
        for mnemonic in signed_results:
            with self.subTest(mnemonic=mnemonic):
                self.assertEqual(
                    self.register_result_extension(mnemonic),
                    "RegisterSignExtend",
                )


if __name__ == "__main__":
    unittest.main()
