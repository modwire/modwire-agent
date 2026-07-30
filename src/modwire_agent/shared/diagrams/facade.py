import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, ClassVar

from modwire_mermaid import ModwireMermaid, ModwireMermaidFactory
from modwire_mermaid.architecture.diagram import ModwireArchitectureDiagram
from modwire_mermaid.class_diagram.diagram import ModwireClassDiagram
from modwire_mermaid.contracts import ModwireBaseDiagram, ModwireDiagramError
from modwire_mermaid.event_modeling.diagram import ModwireEventModel
from modwire_mermaid.file_tree.diagram import ModwireFileTree
from modwire_mermaid.flowchart.diagram import ModwireFlowchart
from modwire_mermaid.mindmap.diagram import ModwireMindmap
from modwire_mermaid.sequence.diagram import ModwireSequenceDiagram
from modwire_mermaid.state.diagram import ModwireStateDiagram
from modwire_mermaid.swimlane.diagram import ModwireSwimlaneDiagram
from modwire_mermaid.timeline.diagram import ModwireTimeline
from modwire_mermaid.user_journey.diagram import ModwireUserJourney
from pydantic import ValidationError
from wireup import injectable

from .errors import DiagramsError

Diagram = ModwireBaseDiagram
DiagramType = type[Diagram]


@injectable
@dataclass(frozen=True)
class DiagramsService:
    _types: ClassVar[dict[str, DiagramType]] = {
        "architecture": ModwireArchitectureDiagram,
        "class_diagram": ModwireClassDiagram,
        "event_modeling": ModwireEventModel,
        "file_tree": ModwireFileTree,
        "flowchart": ModwireFlowchart,
        "mindmap": ModwireMindmap,
        "sequence": ModwireSequenceDiagram,
        "state": ModwireStateDiagram,
        "swimlane": ModwireSwimlaneDiagram,
        "timeline": ModwireTimeline,
        "user_journey": ModwireUserJourney,
    }

    _compiler: ModwireMermaid = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_compiler", ModwireMermaidFactory.standard())

    def get_ids(self) -> list[str]:
        return sorted(self._types)

    def get_schema(self, diagram_id: str) -> dict[str, Any]:
        return self._get_type(diagram_id).model_json_schema()

    def validate(self, diagram_id: str, document: Mapping[str, Any]) -> Diagram:
        try:
            return self._get_type(diagram_id).model_validate_json(json.dumps(document))
        except (ModwireDiagramError, TypeError, ValidationError) as error:
            raise DiagramsError(str(error)) from error

    def recognize(self, content: str) -> None:
        for diagram_type in self._types.values():
            try:
                diagram_type.model_validate_json(content)
            except (ModwireDiagramError, TypeError, ValidationError):
                continue
            return
        raise DiagramsError("Unsupported diagram content.")

    def compile(self, diagram_id: str, document: Mapping[str, Any]) -> str:
        try:
            return self._compiler.compile(self.validate(diagram_id, document))
        except ModwireDiagramError as error:
            raise DiagramsError(str(error)) from error

    def _get_type(self, diagram_id: str) -> DiagramType:
        try:
            return self._types[diagram_id]
        except KeyError as error:
            raise DiagramsError(f"Unsupported diagram ID: {diagram_id!r}") from error
