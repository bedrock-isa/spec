import tempfile
import unittest
from pathlib import Path

from engine.inventory import DirectoryInventory


class DirectoryInventoryTest(unittest.TestCase):
    def test_empty_undeclared_directory_is_not_an_authored_member(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "members.yaml"
            members = root / "members"
            members.mkdir()
            (members / "stale").mkdir()
            source.write_text("members: []\n", encoding="utf-8")

            inventory = DirectoryInventory.inspect(
                owner="base",
                kind="member",
                source=source,
                root=members,
                key="members",
            )

        self.assertEqual(inventory.actual, ())
        self.assertEqual(inventory.undeclared, ())


if __name__ == "__main__":
    unittest.main()
