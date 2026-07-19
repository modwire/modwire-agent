from ninja import Schema

from .preview_file import PreviewFileOut


class ScaffoldingPreviewOut(Schema):
    files: list[PreviewFileOut]
