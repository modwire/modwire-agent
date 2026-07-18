from enum import Enum


class VariableType(str, Enum):
    BOOL = "bool"
    DICT = "dict"
    FLOAT = "float"
    INT = "int"
    LIST = "list"
    STR = "str"

    def __str__(self) -> str:
        return str(self.value)
