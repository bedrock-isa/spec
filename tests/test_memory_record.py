import shutil
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from engine.memory_record import MemoryRecordCatalog, MemoryRecordError
from engine.reference import Reference
from engine.render.memory_record import MemoryRecordProjection


class MemoryRecordCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"

    def test_derives_layout_and_display_height_from_ordered_components(self) -> None:
        with self.fixture() as directory:
            catalog = MemoryRecordCatalog.load(directory)
            record = catalog.resolve("base.records.SAMPLE")
            projection = MemoryRecordProjection.create(record)

            self.assertEqual(record.payload_bytes(8), 16)
            self.assertEqual(record.total_bytes(8), 16)
            self.assertEqual(record.payload_bytes(16), 28)
            self.assertEqual(record.total_bytes(16), 32)
            self.assertEqual(projection.components[1].offset.constant, 4)
            self.assertEqual(
                tuple(row.index for row in projection.components[1].rows),
                (0, 1, None, 4, 5),
            )
            self.assertEqual(
                tuple(row.height for row in projection.components[1].rows),
                (Fraction(1),) * 5,
            )
            self.assertIsNotNone(projection.padding)
            assert projection.padding is not None
            self.assertEqual(projection.padding.values, (0, 4))
            self.assertEqual(projection.padding.height, 1)

    def test_rejects_undeclared_member_directory(self) -> None:
        with self.fixture() as directory:
            (Path(directory) / "records/EXTRA").mkdir()

            with self.assertRaises(ValueError):
                MemoryRecordCatalog.load(directory)

    def test_rejects_symbolic_size_that_is_not_whole_bytes(self) -> None:
        with self.fixture() as directory:
            source = Path(directory) / "records/SAMPLE/record.yaml"
            source.write_text(
                self.record_source.replace("values: [8, 16]", "values: [8, 10]"),
                encoding="utf-8",
            )

            with self.assertRaises(MemoryRecordError):
                MemoryRecordCatalog.load(directory)

    def test_rejects_overlapping_stored_bit_fields(self) -> None:
        with self.fixture() as directory:
            source = Path(directory) / "records/SAMPLE/record.yaml"
            source.write_text(
                self.record_source.replace(
                    "      bits: 8\n",
                    "      bits: 8\n"
                    "    - id: OTHER\n"
                    "      label: Other\n"
                    "      lsb: 7\n"
                    "      bits: 2\n",
                ),
                encoding="utf-8",
            )

            with self.assertRaises(MemoryRecordError):
                MemoryRecordCatalog.load(directory)

    def test_rejects_stored_bit_field_outside_component(self) -> None:
        with self.fixture() as directory:
            source = Path(directory) / "records/SAMPLE/record.yaml"
            source.write_text(
                self.record_source.replace("      bits: 8\n", "      bits: 33\n"),
                encoding="utf-8",
            )

            with self.assertRaises(MemoryRecordError):
                MemoryRecordCatalog.load(directory)

    @property
    def record_source(self) -> str:
        return (
            "id: SAMPLE\n"
            "name: Sample Record\n"
            "alignment_bytes: 16\n"
            "parameter:\n"
            "  id: B\n"
            "  description: sample width in bytes\n"
            "  values: [8, 16]\n"
            "components:\n"
            "- id: HEADER\n"
            "  label: Header\n"
            "  element_bytes: 4\n"
            "  bit_format:\n"
            "    bits: 32\n"
            "    unassigned: zero\n"
            "    fields:\n"
            "    - id: VALUE\n"
            "      label: Value\n"
            "      lsb: 0\n"
            "      bits: 8\n"
            "- id: ITEMS\n"
            "  label: I\n"
            "  count: 6\n"
            "  element_bytes:\n"
            "    parameter: B\n"
            "    divisor: 4\n"
        )

    def fixture(self) -> tempfile.TemporaryDirectory[str]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schemas").mkdir()
        (root / "extensions").mkdir()
        (root / "records/SAMPLE").mkdir(parents=True)
        shutil.copy2(
            self.isa_root / "schemas/memory-record.yaml",
            root / "schemas/memory-record.yaml",
        )
        (root / "extensions/extensions.yaml").write_text(
            "extensions: []\n", encoding="utf-8"
        )
        (root / "records/records.yaml").write_text(
            "records: [SAMPLE]\n", encoding="utf-8"
        )
        (root / "records/SAMPLE/record.yaml").write_text(
            self.record_source, encoding="utf-8"
        )
        return temporary


if __name__ == "__main__":
    unittest.main()
