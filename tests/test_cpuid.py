import unittest

from engine.cpuid import compose_selector


class CpuidCatalogTest(unittest.TestCase):
    def test_composes_architectural_selector_fields(self) -> None:
        self.assertEqual(
            compose_selector(1, 1, 0x0043),
            0x0000000100010043,
        )

if __name__ == "__main__":
    unittest.main()
