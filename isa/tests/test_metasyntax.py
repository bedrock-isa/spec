import unittest

from engine.encoding_metasyntax import (
    EncodingMetasyntax,
    EncodingMetasyntaxError,
)
from engine.instruction_metasyntax import (
    InstructionMetasyntax,
    InstructionMetasyntaxError,
)
from engine.metasyntax import Metasyntax, MetasyntaxError


class MetasyntaxTest(unittest.TestCase):
    def test_concrete_values_share_one_api(self) -> None:
        values = (
            EncodingMetasyntax.parse(["10aa", "01"]),
            InstructionMetasyntax.parse("ADD.Q Rn(s), Rn(d)"),
        )

        for value in values:
            with self.subTest(type=type(value).__name__):
                self.assertIsInstance(value, Metasyntax)
                self.assertIs(type(value).parse(value), value)
                self.assertIsNone(value.validate())
                self.assertEqual(str(value), value.code)

    def test_concrete_errors_share_one_base(self) -> None:
        self.assertTrue(issubclass(EncodingMetasyntaxError, MetasyntaxError))
        self.assertTrue(issubclass(InstructionMetasyntaxError, MetasyntaxError))


if __name__ == "__main__":
    unittest.main()
