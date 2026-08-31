import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from engine.check import EventValidator
from engine.event import EventCatalog, compose_event_code
from engine.extension import ExtensionSetCatalog
from engine.reference import Reference


class EventCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"
        cls.events = EventCatalog.load(
            cls.isa_root, ExtensionSetCatalog.load(cls.isa_root)
        )

    def test_loads_canonical_page_event(self) -> None:
        events = self.events

        page = events.references.events[
            Reference.parse("base.events.EXCEPTION.PAGE_PERMISSION_VIOLATION")
        ]
        self.assertEqual(page.code, 0x21)
        self.assertEqual(page.family, "ADDRESS_TRANSLATION")
        self.assertEqual(page.frame, "page")
        self.assertIn("WALK_LEVEL", page.payload)

    def test_extension_events_overlay_the_base_exception_class(self) -> None:
        events = self.events
        fp_class = events.references.classes[Reference.parse("FP.events.EXCEPTION")]
        vector_class = events.references.classes[
            Reference.parse("VECTOR.events.EXCEPTION")
        ]

        self.assertIs(
            events.root_class(fp_class),
            events.references.classes[Reference.parse("base.events.EXCEPTION")],
        )
        self.assertIs(events.root_class(vector_class), events.root_class(fp_class))
        self.assertEqual(
            events.references.events[
                Reference.parse("FP.events.EXCEPTION.FLOATING_POINT_EXCEPTION")
            ].payload,
            ("FP_EXCEPTION_FLAGS",),
        )

    def test_composes_event_codes(self) -> None:
        self.assertEqual(compose_event_code(0, 0x21), 0x00000021)
        self.assertEqual(compose_event_code(2, 7), 0x02000007)

    def test_resolved_event_joins_overlay_root_and_composed_code(self) -> None:
        resolved = next(
            item
            for item in self.events.resolved_events()
            if item.event.id == "FLOATING_POINT_EXCEPTION"
        )

        self.assertEqual(resolved.owner, "FP")
        self.assertEqual(
            resolved.event_class.reference, Reference.parse("FP.events.EXCEPTION")
        )
        self.assertEqual(
            resolved.root_class.reference, Reference.parse("base.events.EXCEPTION")
        )
        self.assertEqual(resolved.code.class_value, 0)
        self.assertEqual(resolved.code.event_selector, resolved.event.code)
        self.assertEqual(
            resolved.code.value,
            compose_event_code(resolved.code.class_value, resolved.event.code),
        )

    def test_validator_reports_fixed_and_external_selector_errors(self) -> None:
        cases = (
            (
                "extensions/FP/events/classes/EXCEPTION/events/"
                "FLOATING_POINT_EXCEPTION/event.yaml",
                lambda document: document.update(code=0x50),
                "event.code.overlap",
            ),
            (
                "events/classes/EXCEPTION/events/DEBUG_TRACE/event.yaml",
                lambda document: document.pop("code"),
                "event.code.missing",
            ),
            (
                "events/classes/INTERRUPT/events/INTERRUPT/event.yaml",
                lambda document: document.update(code=1),
                "event.code.external-selector",
            ),
        )

        for relative, mutate, expected in cases:
            with self.subTest(code=expected), self.event_fixture() as directory:
                root = Path(directory)
                path = root / relative
                document = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(document)
                path.write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                catalog = EventCatalog.load(root, ExtensionSetCatalog.load(root))
                codes = [item.code for item in EventValidator().validate(catalog)]
                self.assertIn(expected, codes)

    def event_fixture(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schemas").mkdir()
        (root / "extensions").mkdir()
        for schema in ("event-class.yaml", "event.yaml"):
            shutil.copy2(self.isa_root / "schemas" / schema, root / "schemas" / schema)
        shutil.copytree(self.isa_root / "events", root / "events")
        shutil.copy2(
            self.isa_root / "extensions/extensions.yaml",
            root / "extensions/extensions.yaml",
        )
        for extension_id in ExtensionSetCatalog.load(self.isa_root).declared:
            destination = root / "extensions" / extension_id
            destination.mkdir()
            source = self.isa_root / "extensions" / extension_id / "events"
            if source.is_dir():
                shutil.copytree(source, destination / "events")
        return temporary


if __name__ == "__main__":
    unittest.main()
