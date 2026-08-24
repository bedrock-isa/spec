"""Owner-unit checks for strict finite vector-example diagram sources."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import unittest

import yaml


TOOLS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_ROOT))

import site_visuals  # noqa: E402
import site_markdown  # noqa: E402
from site_backend import PageRegistry, PageSpec  # noqa: E402
import vector_diagrams  # noqa: E402
import gen_docs  # noqa: E402


class VectorDiagramTests(unittest.TestCase):
    def source(self, root: Path, *, scalable: bool = True) -> Path:
        path = root / "example.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "lane-map",
                    "view": {"visible_bytes": 16, "lane_order": "right-to-left", "scalable": scalable},
                    "rows": [
                        {"id": "old", "label": "old", "role": "destination-before", "element_bits": 16,
                         "cells": [{"value": f"d{index}", "effect": "copy"} for index in range(8)]},
                        {"id": "new", "label": "new", "role": "destination-after", "element_bits": 16,
                         "cells": [{"value": f"d{index}", "effect": "preserve"} for index in range(8)]},
                    ],
                    "edges": [
                        {"from_row": "old", "from_cell": index, "to_row": "new", "to_cell": index, "effect": "preserve"}
                        for index in range(8)
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def predicate_range_source(self, root: Path) -> Path:
        path = root / "predicate-range.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "predicate-range",
                    "view": {"visible_bytes": 16, "lane_order": "right-to-left", "scalable": True},
                    "count": {"label": "count", "value": 4},
                    "result": {
                        "label": "result",
                        "element_bits": 16,
                        "cells": [
                            {"value": f"p{index}", "effect": "set" if index < 4 else "clear"}
                            for index in range(8)
                        ],
                    },
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def detailed_width_source(self, root: Path, container_bits: int = 16) -> Path:
        path = root / "detailed-width.yaml"
        container_count = vector_diagrams.VISIBLE_BYTES * 8 // container_bits
        field_bits = container_bits // 2
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "width-map",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": True,
                    },
                    "container_bits": container_bits,
                    "rows": [
                        {
                            "id": "source",
                            "label": "source Vn",
                            "role": "source",
                            "containers": [
                                {
                                    "cells": [
                                        {
                                            "value": f"x{index}",
                                            "effect": "ignored",
                                            "appearance": "discarded",
                                            "bits": field_bits,
                                        },
                                        {
                                            "value": f"n{index}",
                                            "effect": "copy",
                                            "appearance": "source",
                                            "bits": field_bits,
                                        },
                                    ]
                                }
                                for index in range(container_count)
                            ],
                        },
                        {
                            "id": "result",
                            "label": "Vd",
                            "role": "destination-after",
                            "containers": [
                                {
                                    "cells": [
                                        {
                                            "value": "sext(n0)" if index == 0 else f"d{index}",
                                            "effect": "sign-fill" if index == 0 else "preserve",
                                            "appearance": "source" if index == 0 else "old",
                                            "bits": container_bits,
                                        }
                                    ]
                                }
                                for index in range(container_count)
                            ],
                        },
                        {
                            "id": "predicate",
                            "label": "predicate Pp",
                            "role": "predicate",
                            "element_bits": 8,
                            "cells": [
                                {
                                    "value": "1" if index == 0 else "x",
                                    "effect": "set" if index == 0 else "ignored",
                                    "appearance": "predicate-on" if index == 0 else "dont-care",
                                }
                                for index in range(16)
                            ],
                        },
                    ],
                    "edges": [
                        {
                            "from_row": "source",
                            "from_container": 0,
                            "from_cell": 1,
                            "to_row": "result",
                            "to_container": 0,
                            "to_cell": 0,
                            "effect": "sign-fill",
                            "display": "expansion-guide",
                        }
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def predicate_width_source(
        self, root: Path, *, source_bits: int = 16, high: bool = False
    ) -> Path:
        path = root / "predicate-width.yaml"
        packing = source_bits == 16
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "predicate-width",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": False,
                    },
                    "source_element_bits": source_bits,
                    "source": {"label": "source Pn"},
                    "result": {
                        "label": "new Pq",
                        "write": "complete",
                        "element_bits": 8 if packing else 16,
                        "mapping": {
                            "source_start": (
                                0
                                if packing or not high
                                else "destination-lanes"
                            ),
                            "destination_start": (
                                "source-lanes" if packing and high else 0
                            ),
                            "count": (
                                "source-lanes" if packing else "destination-lanes"
                            ),
                        },
                    },
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def predicate_lane_map_source(
        self, root: Path, *, scalable: bool = True, with_vector: bool = False
    ) -> Path:
        path = root / "predicate-lane-map.yaml"

        def predicate_groups(prefix: str, appearance: str) -> list[dict[str, object]]:
            return [
                {
                    "cells": [
                        {
                            "value": f"{prefix}[{index}]",
                            "effect": "copy",
                            "appearance": appearance,
                            "bits": 8,
                        },
                        {
                            "value": "x",
                            "effect": "ignored",
                            "appearance": "dont-care",
                            "bits": 8,
                        },
                    ]
                }
                for index in range(8)
            ]

        result_groups = [
            {
                "cells": [
                    {
                        "value": f"d[{index}]",
                        "effect": "copy",
                        "appearance": "predicate-result",
                        "bits": 8,
                    },
                    {
                        "value": "0",
                        "effect": "zero",
                        "appearance": "zero",
                        "bits": 8,
                    },
                ]
            }
            for index in range(8)
        ]
        rows = [
            {
                "id": "old",
                "label": "old Pd",
                "role": "destination-before",
                "storage": "predicate",
                "element_bits": 16,
                "groups": predicate_groups("d", "old"),
            },
            {
                "id": "result",
                "label": "new Pd",
                "role": "destination-after",
                "storage": "predicate",
                "element_bits": 16,
                "groups": result_groups,
            },
        ]
        edges = [
            {
                "from_row": "old",
                "from_group": index,
                "from_cell": 0,
                "to_row": "result",
                "to_group": index,
                "to_cell": 0,
                "display": "transfer",
            }
            for index in range(8)
        ]
        if with_vector:
            rows.append(
                {
                    "id": "indices",
                    "label": "indices Vn",
                    "role": "source",
                    "storage": "vector",
                    "element_bits": 16,
                    "groups": [
                        {
                            "cells": [
                                {
                                    "value": str(index),
                                    "effect": "copy",
                                    "appearance": "source",
                                    "bits": 16,
                                }
                            ]
                        }
                        for index in range(8)
                    ],
                }
            )
            edges.extend(
                {
                    "from_row": "indices",
                    "from_group": index,
                    "from_cell": 0,
                    "to_row": "result",
                    "to_group": index,
                    "to_cell": 0,
                    "display": "control",
                }
                for index in range(8)
            )
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "predicate-lane-map",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": scalable,
                    },
                    "rows": rows,
                    "edges": edges,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def stateful_predicate_range_source(self, root: Path) -> Path:
        path = root / "stateful-predicate-range.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "predicate-range",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": True,
                    },
                    "states": [
                        {
                            "id": "remaining",
                            "label": "remaining Rr",
                            "before": "4",
                            "after": "0",
                            "anchor": "end",
                            "after_side": "left",
                        },
                        {
                            "id": "offset",
                            "label": "offset Rs",
                            "before": "2",
                            "after": "0",
                            "anchor": "start",
                            "after_side": "right",
                        },
                    ],
                    "range": {"start": 2, "end": 6},
                    "result": {
                        "label": "new Pn",
                        "element_bits": 16,
                        "groups": [
                            {
                                "cells": [
                                    {
                                        "value": "1" if 2 <= index < 6 else "0",
                                        "effect": "copy" if 2 <= index < 6 else "zero",
                                        "appearance": (
                                            "predicate-result" if 2 <= index < 6 else "zero"
                                        ),
                                        "bits": 8,
                                    },
                                    {
                                        "value": "0",
                                        "effect": "zero",
                                        "appearance": "zero",
                                        "bits": 8,
                                    },
                                ]
                            }
                            for index in range(8)
                        ],
                    },
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def scalar_bridge_source(self, root: Path) -> Path:
        path = root / "scalar-bridge.yaml"
        cells = [
            {"value": f"d{index}", "effect": "preserve", "appearance": "old"}
            for index in range(8)
        ]
        cells[3] = {"value": "x", "effect": "copy", "appearance": "selected-source"}
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "scalar-bridge",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": True,
                    },
                    "rows": [
                        {
                            "id": "result",
                            "label": "Vd",
                            "role": "destination-after",
                            "element_bits": 16,
                            "cells": cells,
                        }
                    ],
                    "scalars": [
                        {"id": "source", "label": "source Rn", "role": "source", "value": "x"},
                        {"id": "index", "label": "index Rn", "role": "index", "value": "3"},
                    ],
                    "connections": [
                        {
                            "from_kind": "scalar",
                            "from_id": "source",
                            "to_kind": "row",
                            "to_id": "result",
                            "to_cell": 3,
                            "display": "transfer",
                        },
                        {
                            "from_kind": "scalar",
                            "from_id": "index",
                            "to_kind": "row",
                            "to_id": "result",
                            "to_cell": 3,
                            "display": "control",
                        },
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def scalar_extract_bridge_source(self, root: Path) -> Path:
        path = self.scalar_bridge_source(root)
        source = yaml.safe_load(path.read_text(encoding="utf-8"))
        source["rows"][0]["id"] = "source"
        source["rows"][0]["label"] = "source Vn"
        source["rows"][0]["role"] = "source"
        source["rows"][0]["cells"] = [
            {
                "value": f"v{index}",
                "effect": "copy",
                "appearance": "selected-source" if index == 3 else "source",
            }
            for index in range(8)
        ]
        source["scalars"] = [
            {"id": "result", "label": "new Rn", "role": "destination", "value": "zext(v[i])"},
            {"id": "index", "label": "index Rn", "role": "index", "value": "i"},
        ]
        source["connections"] = [
            {
                "from_kind": "row",
                "from_id": "source",
                "from_cell": 3,
                "to_kind": "scalar",
                "to_id": "result",
                "display": "transfer",
            },
            {
                "from_kind": "scalar",
                "from_id": "index",
                "to_kind": "row",
                "to_id": "source",
                "to_cell": 3,
                "display": "control",
            },
        ]
        path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
        return path

    @staticmethod
    def predicate_bytes(selected: set[int], element_bytes: int) -> list[dict[str, str]]:
        return [
            {
                "value": "1" if index // element_bytes in selected else "0",
                "effect": "set" if index // element_bytes in selected else "clear",
                "appearance": (
                    "predicate-on" if index // element_bytes in selected else "predicate-off"
                ),
            }
            if index % element_bytes == 0
            else {"value": "x", "effect": "ignored", "appearance": "dont-care"}
            for index in range(16)
        ]

    def memory_lanes_source(self, root: Path) -> Path:
        path = root / "memory-lanes.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "memory-lanes",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": True,
                    },
                    "element_bits": 64,
                    "base": {"label": "source base", "value": "Rb"},
                    "address": {
                        "label": "address",
                        "cells": [
                            {"value": "[Rb]", "effect": "copy", "appearance": "source"},
                            {"value": "--", "effect": "ignored", "appearance": "no-access"},
                        ],
                    },
                    "memory": {
                        "label": "memory read",
                        "cells": [
                            {"value": "m0", "effect": "copy", "appearance": "source"},
                            {"value": "--", "effect": "ignored", "appearance": "no-access"},
                        ],
                    },
                    "result": {
                        "label": "Vd",
                        "cells": [
                            {"value": "m0", "effect": "copy", "appearance": "source"},
                            {"value": "d1", "effect": "preserve", "appearance": "old"},
                        ],
                    },
                    "predicate": {
                        "label": "predicate Pp",
                        "element_bits": 8,
                        "cells": self.predicate_bytes({0}, 8),
                    },
                    "connections": [
                        {"from_row": "address", "from_cell": 0, "to_row": "memory", "to_cell": 0, "display": "control"},
                        {"from_row": "memory", "from_cell": 0, "to_row": "result", "to_cell": 0, "display": "transfer"},
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def reduction_source(self, root: Path) -> Path:
        path = root / "reduction.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "reduction",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": True,
                    },
                    "element_bits": 32,
                    "predicate": {
                        "label": "predicate Pp",
                        "element_bits": 8,
                        "cells": self.predicate_bytes({0, 2}, 4),
                    },
                    "source": {
                        "label": "source Vn",
                        "cells": [
                            {"value": "v0", "effect": "copy", "appearance": "source"},
                            {"value": "v1", "effect": "ignored", "appearance": "discarded"},
                            {"value": "v2", "effect": "copy", "appearance": "source"},
                            {"value": "v3", "effect": "ignored", "appearance": "discarded"},
                        ],
                    },
                    "selected": [0, 2],
                    "fold": {"label": "fold", "terms": ["0", "v0", "v2"], "continuation": True},
                    "result": {"label": "new Rn", "value": "sum"},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def conversion_map_source(self, root: Path) -> Path:
        path = root / "conversion-map.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "kind": "conversion-map",
                    "view": {
                        "visible_bytes": 16,
                        "lane_order": "right-to-left",
                        "scalable": True,
                    },
                    "container_bits": 64,
                    "source": {
                        "label": "source D values",
                        "element_bits": 64,
                        "containers": [
                            {"cells": [{"value": f"d{index}", "effect": "copy", "appearance": "source", "bits": 64}]}
                            for index in range(2)
                        ],
                    },
                    "result": {
                        "label": "new H fields",
                        "element_bits": 16,
                        "containers": [
                            {
                                "cells": [
                                    {"value": "old0", "effect": "preserve", "appearance": "old", "bits": 48},
                                    {"value": "H(d0)", "effect": "copy", "appearance": "source", "bits": 16},
                                ]
                            },
                            {"cells": [{"value": "old1", "effect": "preserve", "appearance": "old", "bits": 64}]},
                        ],
                    },
                    "predicate": {
                        "label": "predicate Pp",
                        "element_bits": 8,
                        "cells": self.predicate_bytes({0}, 8),
                    },
                    "connections": [
                        {
                            "from_row": "source",
                            "from_container": 0,
                            "from_cell": 0,
                            "to_row": "result",
                            "to_container": 0,
                            "to_cell": 1,
                            "effect": "copy",
                            "display": "transfer",
                        }
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def test_lane_map_edges_are_only_the_authored_visible_transfers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.source(Path(directory))
            source = yaml.safe_load(path.read_text(encoding="utf-8"))
            source["edges"].pop()
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
            self.assertEqual(len(vector_diagrams.load(path).edges), 7)

    def test_scalable_boolean_controls_continuation_rendering(self) -> None:
        for scalable in (False, True):
            with self.subTest(scalable=scalable), tempfile.TemporaryDirectory() as directory:
                rendered = vector_diagrams.render_tikz(
                    vector_diagrams.load(self.source(Path(directory), scalable=scalable))
                )
                self.assertEqual("vectorExampleContinuation" in rendered, scalable)

        with tempfile.TemporaryDirectory() as directory:
            path = self.source(Path(directory))
            source = yaml.safe_load(path.read_text(encoding="utf-8"))
            source["view"]["scalable"] = "true"
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, r"view\.scalable must be a boolean"):
                vector_diagrams.load(path)

        with tempfile.TemporaryDirectory() as directory:
            path = self.predicate_range_source(Path(directory))
            source = yaml.safe_load(path.read_text(encoding="utf-8"))
            source["view"]["scalable"] = False
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, r"predicate-range requires scalable"):
                vector_diagrams.load(path)

    def test_rejects_closed_key_computed_expression_field(self) -> None:
        mutations = (
            (
                "computed lane-map result",
                self.source,
                lambda source: source.__setitem__("result", {"select": "computed"}),
                r"root keys",
            ),
            (
                "width-map terminal result",
                self.source,
                lambda source: (
                    source.__setitem__("kind", "width-map"),
                    source.__setitem__(
                        "terminal_results",
                        [{"to_row": "new", "to_cell": 0, "effect": "zero"}],
                    ),
                ),
                r"width-map root keys",
            ),
            (
                "predicate-range terminal result",
                self.predicate_range_source,
                lambda source: source.__setitem__(
                    "terminal_results",
                    [{"to_row": "result", "to_cell": 0, "effect": "zero"}],
                ),
                r"root keys",
            ),
        )
        for label, source_factory, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = source_factory(Path(directory))
                source = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(source)
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, diagnostic):
                    vector_diagrams.load(path)

    def test_rejects_invalid_edge_boundaries_ownership_and_effect(self) -> None:
        mutations = (
            ("source bound", lambda source: source["edges"][0].__setitem__("from_cell", 99), "out of bounds"),
            ("target bound", lambda source: source["edges"][0].__setitem__("to_cell", 99), "out of bounds"),
            ("target row", lambda source: source["edges"][0].__setitem__("to_row", "old"), "invalid cell reference"),
            ("bool index", lambda source: source["edges"][0].__setitem__("from_cell", True), "must be an integer"),
            ("duplicate", lambda source: source["edges"][1].__setitem__("to_cell", 0), "one valid result target"),
            ("effect", lambda source: source["edges"][0].__setitem__("effect", "copy"), "classification"),
            *(
                (
                    f"unsupported matching {effect} effect",
                    lambda source, effect=effect: (
                        source["rows"][1]["cells"][0].__setitem__("effect", effect),
                        source["edges"][0].__setitem__("effect", effect),
                    ),
                    "renderable transfer classification",
                )
                for effect in sorted(vector_diagrams.CELL_EFFECTS - vector_diagrams.TRANSFER_EFFECTS)
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = self.source(Path(directory))
                source = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(source)
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, diagnostic):
                    vector_diagrams.load(path)

    def test_rejects_boolean_integer_scalars(self) -> None:
        mutations = (
            (
                "lane element bits",
                self.source,
                lambda source: source["rows"][0].__setitem__("element_bits", True),
                r"rows\[0\]\.element_bits must be an integer",
            ),
            (
                "predicate range count",
                self.predicate_range_source,
                lambda source: source["count"].__setitem__("value", True),
                r"count\.value must be an integer",
            ),
        )
        for label, source_factory, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = source_factory(Path(directory))
                source = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(source)
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, diagnostic):
                    vector_diagrams.load(path)

    def test_rejects_multiple_result_rows_and_escapes_tex_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.source(Path(directory))
            source = yaml.safe_load(path.read_text(encoding="utf-8"))
            source["rows"].append(dict(source["rows"][1], id="another"))
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, r"exactly one destination-after"):
                vector_diagrams.load(path)
        with tempfile.TemporaryDirectory() as directory:
            path = self.source(Path(directory))
            source = yaml.safe_load(path.read_text(encoding="utf-8"))
            source["rows"][0]["label"] = r"\\input{hostile}_&"
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
            rendered = vector_diagrams.render_tikz(vector_diagrams.load(path))
            self.assertIn(r"\textbackslash{}input\{hostile\}\_\&", rendered)

    def test_lane_map_preserves_authored_row_order_and_cell_appearance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.source(Path(directory))
            source = yaml.safe_load(path.read_text(encoding="utf-8"))
            source["view"]["scalable"] = False
            source["rows"][0]["cells"][0]["appearance"] = "old"
            source["rows"][1]["cells"][0]["appearance"] = "source"
            source["rows"].insert(
                1,
                {
                    "id": "predicate",
                    "label": "predicate Pp",
                    "role": "predicate",
                    "element_bits": 8,
                    "cells": [
                        {
                            "value": "1" if index == 0 else "x",
                            "effect": "set" if index == 0 else "ignored",
                            "appearance": "predicate-on" if index == 0 else "dont-care",
                        }
                        for index in range(16)
                    ],
                },
            )
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
            rendered = vector_diagrams.render_tikz(vector_diagrams.load(path))
            self.assertLess(rendered.index("{old}"), rendered.index("{predicate Pp}"))
            self.assertLess(rendered.index("{predicate Pp}"), rendered.index("{new}"))
            self.assertIn("vectorExampleOld", rendered)
            self.assertIn("vectorExampleSource", rendered)
            self.assertIn("vectorExamplePredicateOn", rendered)
            self.assertIn("fixed example: VLEN = 16 bytes", rendered)

            source["rows"][0]["cells"][0]["appearance"] = "computed"
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(
                vector_diagrams.VectorDiagramError, r"registered cell appearance"
            ):
                vector_diagrams.load(path)

            for variant_only_appearance in ("selected-source", "no-access"):
                source["rows"][0]["cells"][0]["appearance"] = variant_only_appearance
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.subTest(appearance=variant_only_appearance), self.assertRaisesRegex(
                    vector_diagrams.VectorDiagramError, r"registered cell appearance"
                ):
                    vector_diagrams.load(path)

    def test_detailed_width_map_derives_reviewed_container_geometry(self) -> None:
        expected_guides = {
            16: "(7.56,1.08) -- (7.06,0.68)",
            32: "(7.06,1.08) -- (6.06,0.68)",
            64: "(6.06,1.08) -- (4.06,0.68)",
        }
        for container_bits, expected_guide in expected_guides.items():
            with self.subTest(container_bits=container_bits), tempfile.TemporaryDirectory() as directory:
                example = vector_diagrams.load(
                    self.detailed_width_source(Path(directory), container_bits)
                )
                self.assertEqual(
                    len(example.rows[0]["containers"]),
                    vector_diagrams.VISIBLE_BYTES * 8 // container_bits,
                )
                rendered = vector_diagrams.render_tikz(example)
                self.assertIn(expected_guide, rendered)
                self.assertIn("vectorExampleDiscarded", rendered)
                self.assertIn("vectorExampleContainer", rendered)
                self.assertIn("vectorExamplePredicateOn", rendered)
                self.assertIn("vectorExampleWidthContinuation", rendered)
                self.assertLess(rendered.index("{source Vn}"), rendered.index("{Vd}"))
                self.assertLess(rendered.index("{Vd}"), rendered.index("{predicate Pp}"))

    def test_detailed_width_map_rejects_incomplete_or_invalid_structure(self) -> None:
        mutations = (
            (
                "container width",
                lambda source: source.__setitem__("container_bits", 8),
                "one of 16, 32, or 64",
            ),
            (
                "container count",
                lambda source: source["rows"][0]["containers"].pop(),
                "visible containers",
            ),
            (
                "field partition",
                lambda source: source["rows"][0]["containers"][0]["cells"][0].__setitem__("bits", 7),
                "cover exactly 16 bits",
            ),
            (
                "predicate coverage",
                lambda source: source["rows"][2]["cells"].pop(),
                "predicate row must cover 16 bytes",
            ),
            (
                "edge target",
                lambda source: source["edges"][0].__setitem__("to_container", 99),
                "target container is out of bounds",
            ),
            (
                "edge source row",
                lambda source: source["edges"][0].__setitem__("from_row", "result"),
                "source must be the source row",
            ),
            (
                "ignored edge source",
                lambda source: source["rows"][0]["containers"][0]["cells"][1].__setitem__("effect", "ignored"),
                "source cell must not be ignored",
            ),
            (
                "edge presentation",
                lambda source: source["edges"][0].__setitem__("display", "curve"),
                "width-map presentation",
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = self.detailed_width_source(Path(directory))
                source = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(source)
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, diagnostic):
                    vector_diagrams.load(path)

    def test_predicate_width_derives_only_the_reviewed_finite_mappings(self) -> None:
        expected_transfers = {
            (16, False): "(0.75,1.38) -- (4.25,0.68)",
            (16, True): "(0.75,1.38) -- (0.25,0.68)",
            (8, False): "(4.25,1.38) -- (0.75,0.68)",
            (8, True): "(0.25,1.38) -- (0.75,0.68)",
        }
        for (source_bits, high), final_transfer in expected_transfers.items():
            with self.subTest(source_bits=source_bits, high=high), tempfile.TemporaryDirectory() as directory:
                example = vector_diagrams.load(
                    self.predicate_width_source(
                        Path(directory), source_bits=source_bits, high=high
                    )
                )
                rendered = vector_diagrams.render_tikz(example)
                self.assertEqual(
                    tuple(row["role"] for row in example.rows),
                    ("source", "destination-after"),
                )
                self.assertEqual(len(example.edges), 8)
                self.assertEqual(rendered.count("vectorExampleWidthTransferArrow"), 8)
                self.assertEqual(rendered.count("\\path[vectorExampleZero]"), 8)
                self.assertIn(final_transfer, rendered)
                self.assertIn("vectorExamplePredicateResult", rendered)
                self.assertIn("fixed example: VLEN = 16 bytes", rendered)
                self.assertNotIn("Continuation", rendered)
                self.assertLess(
                    rendered.index("\\path[vectorExampleSource]"),
                    rendered.index("\\path[vectorExampleZero]"),
                )

    def test_predicate_width_rejects_broader_or_incomplete_models(self) -> None:
        mutations = (
            (
                "scalable view",
                lambda source: source["view"].__setitem__("scalable", True),
                "fixed 16-byte example view",
            ),
            (
                "unregistered widths",
                lambda source: source.__setitem__("source_element_bits", 32),
                "reviewed 16-to-8 and 8-to-16 examples",
            ),
            (
                "partial result",
                lambda source: source["result"].__setitem__("write", "merge"),
                r"result\.write must be complete",
            ),
            (
                "literal lane count",
                lambda source: source["result"]["mapping"].__setitem__("count", 8),
                "literal must be zero",
            ),
            (
                "wrong lane-count term",
                lambda source: source["result"]["mapping"].__setitem__(
                    "count", "destination-lanes"
                ),
                "count must be source-lanes",
            ),
            (
                "computed mapping",
                lambda source: source["result"]["mapping"].__setitem__(
                    "source_start", {"divide": "lanes"}
                ),
                "must be a non-empty string",
            ),
            (
                "operation selector",
                lambda source: source.__setitem__("operation", "pack-high"),
                "predicate-width root keys",
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = self.predicate_width_source(Path(directory))
                source = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(source)
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, diagnostic):
                    vector_diagrams.load(path)

    def test_predicate_lane_map_preserves_authored_rows_cells_and_edges(self) -> None:
        for scalable in (False, True):
            with self.subTest(scalable=scalable), tempfile.TemporaryDirectory() as directory:
                example = vector_diagrams.load(
                    self.predicate_lane_map_source(
                        Path(directory), scalable=scalable, with_vector=True
                    )
                )
                rendered = vector_diagrams.render_tikz(example)
                self.assertEqual(
                    tuple(row["id"] for row in example.rows),
                    ("old", "result", "indices"),
                )
                self.assertEqual(len(example.edges), 16)
                self.assertEqual(rendered.count("vectorExampleLaneTransferArrow"), 8)
                self.assertEqual(rendered.count("vectorExamplePredicateControlArrow"), 8)
                self.assertLess(rendered.index("{old Pd}"), rendered.index("{new Pd}"))
                self.assertLess(rendered.index("{new Pd}"), rendered.index("{indices Vn}"))
                self.assertEqual(
                    "vectorExamplePredicateLaneContinuation" in rendered,
                    scalable,
                )
                self.assertEqual("fixed example: VLEN = 16 bytes" in rendered, not scalable)

    def test_predicate_lane_map_rejects_incomplete_or_inferred_structure(self) -> None:
        mutations = (
            (
                "expression result",
                lambda source: source.__setitem__("result", {"interleave": []}),
                "predicate-lane-map root keys",
            ),
            (
                "row count",
                lambda source: source["rows"].extend(
                    [
                        dict(source["rows"][0], id="extra-one"),
                        dict(source["rows"][0], id="extra-two"),
                    ]
                ),
                "two or three authored rows",
            ),
            (
                "group coverage",
                lambda source: source["rows"][0]["groups"].pop(),
                "all eight visible W groups",
            ),
            (
                "group partition",
                lambda source: source["rows"][0]["groups"][0]["cells"][0].__setitem__("bits", 7),
                "cover exactly 16 bits",
            ),
            (
                "result nonsignificant bit",
                lambda source: source["rows"][1]["groups"][0]["cells"][1].__setitem__("effect", "ignored"),
                "cleared bits",
            ),
            (
                "ignored edge source",
                lambda source: source["edges"][0].__setitem__("from_cell", 1),
                "displayed source value",
            ),
            (
                "edge target bound",
                lambda source: source["edges"][0].__setitem__("to_group", 8),
                "target group is out of bounds",
            ),
            (
                "duplicate transfer",
                lambda source: source["edges"][1].__setitem__("to_group", 0),
                "duplicates a displayed result connection",
            ),
            (
                "wrong display storage",
                lambda source: source["edges"][0].__setitem__("display", "control"),
                "control source must use vector storage",
            ),
            (
                "missing authored arrow",
                lambda source: source["edges"].pop(),
                "transfers must cover exactly",
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = self.predicate_lane_map_source(Path(directory))
                source = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(source)
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(vector_diagrams.VectorDiagramError, diagnostic):
                    vector_diagrams.load(path)

    def test_new_finite_variants_decode_and_render_declared_primitives(self) -> None:
        cases = (
            (
                "stateful predicate range",
                self.stateful_predicate_range_source,
                "predicate-range",
                ("vectorExampleStateLabel", "vectorExampleRange"),
            ),
            (
                "scalar bridge",
                self.scalar_bridge_source,
                "scalar-bridge",
                ("vectorExampleSelectedSource", "vectorExampleControlArrow"),
            ),
            (
                "memory lanes",
                self.memory_lanes_source,
                "memory-lanes",
                (
                    "vectorExampleNoAccess",
                    "vectorExampleControlArrow",
                    "(6.00,2.33) -- (6.00,1.78)",
                ),
            ),
            (
                "reduction",
                self.reduction_source,
                "reduction",
                ("vectorExampleFold", "vectorExampleEquality"),
            ),
            (
                "conversion map",
                self.conversion_map_source,
                "conversion-map",
                ("vectorExampleContainer", "vectorExampleWidthTransferArrow"),
            ),
        )
        for label, source_factory, variant, rendered_tokens in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                example = vector_diagrams.load(source_factory(Path(directory)))
                self.assertEqual(example.variant, variant)
                rendered = vector_diagrams.render_tikz(example)
                for token in rendered_tokens:
                    self.assertIn(token, rendered)

    def test_new_finite_variants_reject_incomplete_or_inferred_structure(self) -> None:
        mutations = (
            (
                "stateful range classification",
                self.stateful_predicate_range_source,
                lambda source: source["result"]["groups"][2]["cells"][0].__setitem__("value", "0"),
                "does not match the authored active range",
            ),
            (
                "scalar transfer coverage",
                self.scalar_bridge_source,
                lambda source: source["connections"].pop(0),
                "insertion requires exactly one displayed transfer",
            ),
            (
                "scalar insertion index lane",
                self.scalar_bridge_source,
                lambda source: source["connections"][1].__setitem__("to_cell", 2),
                r"connections\[1\]\.to_cell must select the transferred result lane",
            ),
            (
                "scalar extraction transfer",
                self.scalar_extract_bridge_source,
                lambda source: source["connections"].pop(0),
                "extraction requires exactly one displayed transfer",
            ),
            (
                "memory active-access coverage",
                self.memory_lanes_source,
                lambda source: source["connections"].pop(),
                "connections must cover exactly every active access",
            ),
            (
                "memory active predicate classification",
                self.memory_lanes_source,
                lambda source: source["predicate"]["cells"][0].__setitem__("effect", "clear"),
                r"predicate\.cells\[0\] does not match active lane 0",
            ),
            (
                "memory active address appearance",
                self.memory_lanes_source,
                lambda source: source["address"]["cells"][0].__setitem__("appearance", "no-access"),
                r"address\.cells\[0\] does not match active memory lanes",
            ),
            (
                "reduction fold source",
                self.reduction_source,
                lambda source: source["fold"]["terms"].__setitem__(1, "v1"),
                "fold terms after the identity must equal the selected source values",
            ),
            (
                "reduction selected order",
                self.reduction_source,
                lambda source: source.__setitem__("selected", list(reversed(source["selected"]))),
                "selected must list visible lanes in increasing logical-lane order",
            ),
            (
                "conversion equal widths",
                self.conversion_map_source,
                lambda source: source["result"].__setitem__("element_bits", 64),
                "source and result widths must differ",
            ),
            (
                "conversion source element width",
                self.conversion_map_source,
                lambda source: source["source"].__setitem__("element_bits", 32),
                r"source\.containers\[0\]\.cells\[0\]\.bits must equal source\.element_bits",
            ),
            (
                "conversion active predicate classification",
                self.conversion_map_source,
                lambda source: source["predicate"]["cells"][0].__setitem__("effect", "clear"),
                r"predicate\.cells\[0\] does not match active lane 0",
            ),
            (
                "conversion result element width",
                self.conversion_map_source,
                lambda source: source["result"].__setitem__("element_bits", 32),
                r"result\.containers\[0\]\.cells\[1\]\.bits must equal result\.element_bits",
            ),
        )
        for label, source_factory, mutate, diagnostic in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = source_factory(Path(directory))
                source = yaml.safe_load(path.read_text(encoding="utf-8"))
                mutate(source)
                path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(
                    vector_diagrams.VectorDiagramError, diagnostic
                ) as raised:
                    vector_diagrams.load(path)
                self.assertIn(str(path), str(raised.exception))

    def test_scalar_bridge_places_extracted_scalar_at_selected_lane(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.scalar_extract_bridge_source(Path(directory))
            rendered = vector_diagrams.render_tikz(vector_diagrams.load(path))
            self.assertIn("(scalarBridgeResult) at (4.50,0.31)", rendered)
            self.assertIn("(scalarBridgeIndex) at (4.50,2.51)", rendered)

    def test_scalar_bridge_broadcast_uses_source_cells_and_centered_bus(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.scalar_bridge_source(Path(directory))
            source = yaml.safe_load(path.read_text(encoding="utf-8"))
            source["rows"][0]["cells"] = [
                {"value": "x", "effect": "copy", "appearance": "source"}
                for _ in range(8)
            ]
            source["scalars"] = [
                {"id": "source", "label": "source Rn", "role": "source", "value": "x"}
            ]
            source["connections"] = [
                {
                    "from_kind": "scalar",
                    "from_id": "source",
                    "to_kind": "row",
                    "to_id": "result",
                    "to_cell": index,
                    "display": "transfer",
                }
                for index in range(8)
            ]
            path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")

            rendered = vector_diagrams.render_tikz(vector_diagrams.load(path))
            self.assertIn("(scalarBridgeSource) at (4.00,1.41)", rendered)
            self.assertEqual(rendered.count("vectorExampleLaneTransferArrow"), 8)
            self.assertEqual(rendered.count("vectorExampleSource"), 8)

    def test_site_uses_alt_text_while_replacement_retains_caption(self) -> None:
        document = """\\begin{document}
\\section{Instructions}
\\begin{BedrockVectorExample}{2in}{.5cm}{.5cm}{Visible \\texttt{VADD.\\{B\\textbar{}W\\}} caption.}{Distinct \\texttt{VADD.\\{B\\textbar{}W\\}} nonvisual equivalent.}
\\node at (0,0) {x};
\\end{BedrockVectorExample}
\\end{document}
"""
        structure = type("Structure", (), {"sections": (), "instructions": ()})()
        visualized = site_visuals.extract_visuals("reference", document, structure)
        self.assertEqual(
            tuple(visualized.titles.values()),
            ("Distinct VADD.{B|W} nonvisual equivalent.",),
        )
        self.assertIn(r"Visible \texttt{VADD.\{B\textbar{}W\}} caption.", visualized.text)
        self.assertNotIn("Distinct VADD.{B|W} nonvisual equivalent.", visualized.text)

    def test_site_plain_titles_preserve_every_form_metasyntax(self) -> None:
        site_markdown.require_supported_pandoc()
        model = gen_docs.load_model(gen_docs.DEF_ROOT)
        entries = [
            entry
            for entries in model.allocated_by_mnemonic.values()
            for entry in entries
        ]
        forms = [entry.text for entry in entries]
        alternatives = [form for form in forms if "{" in form and "|" in form]
        angle_operands = [form for form in forms if "<" in form and ">" in form]
        self.assertTrue(forms)
        self.assertTrue(alternatives)
        self.assertTrue(angle_operands)
        for form in forms:
            with self.subTest(form=form):
                self.assertEqual(site_visuals._plain_title(gen_docs.tex_code(form)), form)

        document = "\n".join(
            [
                r"\begin{document}",
                *(gen_docs.latex_entry_bit_diagram(entry, entry.text) for entry in entries),
                r"\end{document}",
            ]
        )
        structure = type("Structure", (), {"sections": (), "instructions": ()})()
        visualized = site_visuals.extract_visuals("forms", document, structure)
        with tempfile.TemporaryDirectory() as directory:
            expanded = Path(directory) / "forms.tex"
            expanded.write_text(visualized.text, encoding="utf-8")
            ast = site_markdown.read_pandoc_ast(expanded)

        registry = PageRegistry()
        registry.add_page(
            PageSpec("forms", "Forms", PurePosixPath("forms.md"))
        )
        rendered = site_markdown.render_page_ast(
            site_markdown.PageAst("forms", 1, ast.blocks),
            document="forms",
            title="Forms",
            registry=registry,
            visual_titles=visualized.titles,
            api_version=ast.api_version,
        )
        serialized_alts = [
            line for line in rendered.markdown.splitlines() if line.startswith("![")
        ]
        serialized_captions = [
            line for line in rendered.markdown.splitlines() if line.startswith("**")
        ]
        self.assertEqual(len(serialized_alts), len(forms), "serialized image alt count")
        self.assertEqual(
            len(serialized_captions), len(forms), "serialized caption count"
        )
        for path, lines in (
            ("alt", serialized_alts),
            ("caption", serialized_captions),
        ):
            for form, line in zip(forms, lines):
                with self.subTest(path=path, form=form, serialized=line):
                    self.assertNotIn(r"\<", line)
                    self.assertNotIn(r"\>", line)
        reparsed = subprocess.run(
            [
                "pandoc",
                f"--from={site_markdown.PANDOC_GFM_WRITER}",
                "--to=json",
            ],
            input=rendered.markdown,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(reparsed.returncode, 0, reparsed.stderr)
        markdown_ast = json.loads(reparsed.stdout)

        def inline_text(inlines: list[dict[str, object]]) -> str:
            parts: list[str] = []
            for inline in inlines:
                tag = inline["t"]
                if tag == "Str":
                    parts.append(str(inline["c"]))
                elif tag in {"Space", "SoftBreak", "LineBreak"}:
                    parts.append(" ")
            return "".join(parts)

        alt_texts: list[str] = []
        caption_texts: list[str] = []

        def collect_reader_text(value: object) -> None:
            if isinstance(value, dict):
                tag = value.get("t")
                content = value.get("c")
                if tag == "Image":
                    assert isinstance(content, list)
                    alt_texts.append(inline_text(content[1]))
                    return
                if tag == "Strong":
                    assert isinstance(content, list)
                    caption_texts.append(inline_text(content))
                    return
                for child in value.values():
                    collect_reader_text(child)
            elif isinstance(value, list):
                for child in value:
                    collect_reader_text(child)

        collect_reader_text(markdown_ast["blocks"])
        # This public prefix is owned by latex_entry_bit_diagram; the em dash is
        # part of the observed site-caption regression boundary.
        expected = [f"Format — Instruction format for {form}" for form in forms]
        self.assertEqual(len(alt_texts), len(expected), "image alt count")
        self.assertEqual(len(caption_texts), len(expected), "caption count")
        for path, actual_texts in (
            ("alt", alt_texts),
            ("caption", caption_texts),
        ):
            for form, expected_text, actual_text in zip(forms, expected, actual_texts):
                with self.subTest(path=path, form=form):
                    self.assertEqual(actual_text, expected_text)

    def test_registered_bundle_diagrams_project_all_current_variants(self) -> None:
        model = gen_docs.load_model(gen_docs.DEF_ROOT)
        admitted = [
            item
            for item in model.instructions
            if item.operation and item.operation.artifacts.diagrams
        ]
        variants = set()
        for instruction in admitted:
            operation = instruction.operation
            assert operation is not None and operation.artifacts.bundle_root is not None
            for ref in operation.artifacts.diagrams:
                source = Path(operation.artifacts.bundle_root) / ref.path
                example = vector_diagrams.load(source)
                variants.add(example.variant)
                rendered = gen_docs.latex_operation_diagrams(operation)
                self.assertIn(ref.caption, rendered)
                self.assertIn(ref.alt_text, rendered)
                self.assertNotEqual(ref.caption, ref.alt_text)
                if example.variant == "predicate-width":
                    self.assertIn("{3.20in}{.76cm}{.70cm}", rendered)
                if example.variant == "predicate-lane-map":
                    self.assertIn("{.76cm}{.70cm}", rendered)
            entry = gen_docs.latex_instruction_entry(model, instruction)
            detail = gen_docs.operation_description_tex(operation)
            self.assertIn(
                "\\manualoperationfield{Operation}{"
                + gen_docs.latex_escape(operation.summary)
                + "}",
                entry,
            )
            self.assertEqual(entry.count(detail), 1)
            self.assertLess(
                entry.index("\\manualinstructiondescriptionheading{Detailed Semantics}"),
                entry.index(detail),
            )
            self.assertLess(entry.index(detail), entry.index("\\begin{BedrockVectorExample}"))
        self.assertIn("predicate-width", variants)
        self.assertIn("predicate-lane-map", variants)


if __name__ == "__main__":
    unittest.main()
