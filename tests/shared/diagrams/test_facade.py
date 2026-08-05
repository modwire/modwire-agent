import pytest

from enclosure.shared.diagrams import DiagramsError, DiagramsService


@pytest.fixture
def diagrams() -> DiagramsService:
    return DiagramsService()


def test_lists_supported_diagrams(diagrams: DiagramsService) -> None:
    assert diagrams.get_ids() == [
        "architecture",
        "class_diagram",
        "event_modeling",
        "file_tree",
        "flowchart",
        "mindmap",
        "sequence",
        "state",
        "swimlane",
        "timeline",
        "user_journey",
    ]


def test_returns_diagram_schema(diagrams: DiagramsService) -> None:
    assert diagrams.get_schema("mindmap")["type"] == "object"


def test_validates_and_compiles_diagram(diagrams: DiagramsService) -> None:
    document = {
        "root": {
            "id": "root",
            "label": "root",
            "shape": "default",
            "text_format": "plain",
            "icon_classes": [],
            "css_classes": [],
            "children": [],
        },
        "layout": "",
    }

    diagram = diagrams.validate("mindmap", document)

    assert diagram.root.id == "root"
    assert diagrams.compile("mindmap", document).startswith("mindmap")


def test_rejects_unknown_diagram(diagrams: DiagramsService) -> None:
    with pytest.raises(DiagramsError, match="Unsupported diagram ID"):
        diagrams.get_schema("unknown")
