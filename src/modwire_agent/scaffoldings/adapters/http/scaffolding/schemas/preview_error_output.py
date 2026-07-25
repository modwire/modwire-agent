from ninja import Schema

from .preview_error import PreviewErrorOut


class ScaffoldingPreviewErrorOut(Schema):
    errors: list[PreviewErrorOut]
