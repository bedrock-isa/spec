import unittest
from pathlib import Path

from engine.event import EventCatalog, compose_event_code
from engine.extension import ExtensionSetCatalog


class EventCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1] / "isa"
        cls.events = EventCatalog.load(
            cls.isa_root, ExtensionSetCatalog.load(cls.isa_root)
        )

    def test_class_overlays_resolve_to_numeric_roots(self) -> None:
        for event_class in self.events.references.classes.values():
            root = self.events.root_class(event_class)
            self.assertIsNone(root.extends)
            self.assertIsNotNone(root.value)

    def test_composes_event_codes(self) -> None:
        self.assertEqual(compose_event_code(0, 0x21), 0x00000021)
        self.assertEqual(compose_event_code(2, 7), 0x02000007)

    def test_resolved_events_join_roots_and_composed_codes(self) -> None:
        for resolved in self.events.resolved_events():
            self.assertIs(
                resolved.root_class,
                self.events.root_class(resolved.event_class),
            )
            self.assertEqual(resolved.code.class_value, resolved.root_class.value)
            self.assertEqual(resolved.code.event_selector, resolved.event.code)
            if resolved.event.code is None:
                self.assertIsNone(resolved.code.value)
            else:
                self.assertEqual(
                    resolved.code.value,
                    compose_event_code(
                        resolved.code.class_value, resolved.event.code
                    ),
                )


if __name__ == "__main__":
    unittest.main()
