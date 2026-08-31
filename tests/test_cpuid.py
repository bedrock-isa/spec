import unittest

from engine.cpuid import compose_selector, extension_discovery_leaf_value


class CpuidWireFormatTest(unittest.TestCase):
    def test_extension_directory_slot_determines_discovery_leaf(self) -> None:
        cases = (
            (1, 0, 1),
            (1, 63, 64),
            (2, 0, 65),
            (1023, 63, 65472),
        )
        for directory_index, directory_bit, expected_leaf in cases:
            with self.subTest(index=directory_index, bit=directory_bit):
                self.assertEqual(
                    extension_discovery_leaf_value(
                        directory_index, directory_bit
                    ),
                    expected_leaf,
                )

    def test_composes_architectural_selector_fields(self) -> None:
        self.assertEqual(
            compose_selector(0x89ABCDEF, 0x4567, 0x0123),
            0x89ABCDEF45670123,
        )


if __name__ == "__main__":
    unittest.main()
