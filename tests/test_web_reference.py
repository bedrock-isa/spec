import unittest
from pathlib import PurePosixPath

from engine.site.model import ROOT_PAGE_KEY, SiteModel
from engine.site.navigation import NavigationGroup, PageRegistry, PageSpec


class WebReferenceTest(unittest.TestCase):
    def test_navigation_projects_each_owned_page_once(self) -> None:
        registry = PageRegistry()
        registry.add_page(
            PageSpec(ROOT_PAGE_KEY, "Home", PurePosixPath("index.md"))
        )
        registry.add_page(
            PageSpec(
                "guide:landing",
                "Guide",
                PurePosixPath("guide/index.md"),
                group="guide",
            )
        )
        registry.add_page(
            PageSpec(
                "guide:topic",
                "Topic",
                PurePosixPath("guide/topic.md"),
                group="guide",
                parent="guide:landing",
            )
        )
        site = SiteModel(registry, (NavigationGroup("guide", "Guide"),))

        def outputs(entries: list[dict[str, object]]) -> list[str]:
            projected: list[str] = []
            for entry in entries:
                value = next(iter(entry.values()))
                if isinstance(value, str):
                    projected.append(value)
                elif isinstance(value, list):
                    projected.extend(outputs(value))
                else:
                    self.fail(f"unexpected navigation entry: {entry!r}")
            return projected

        projected = outputs(site.navigation())
        owned = [page.output.as_posix() for page in registry.pages]

        self.assertEqual(sorted(projected), sorted(owned))

if __name__ == "__main__":
    unittest.main()
