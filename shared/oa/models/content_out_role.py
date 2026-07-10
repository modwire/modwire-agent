from enum import Enum

class ContentOutRole(str, Enum):
    HEADING = "heading"
    IMAGE = "image"
    LIST = "list"
    MARKDOWN = "markdown"
    PARAGRAPH = "paragraph"
    SNIPPET = "snippet"
    SUBHEADING = "subheading"

    def __str__(self) -> str:
        return str(self.value)
