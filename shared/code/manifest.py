from typing import Any, ClassVar, Literal, get_args, get_origin

import yaml

from pydantic import BaseModel
from pydantic_core import PydanticUndefined


class CopierManifest(BaseModel):
    min_copier_version: ClassVar[str] = "9.0.0"
    templates_suffix: ClassVar[str] = ".jinja"
    subdirectory: ClassVar[str] = "templates"

    jinja_extensions: ClassVar[list[str]] = [
        "jinja2_slug.SlugExtension",
    ]

    @classmethod
    def to_copier_config(cls) -> dict[str, Any]:
        config: dict[str, Any] = {
            "_min_copier_version": cls.min_copier_version,
            "_templates_suffix": cls.templates_suffix,
            "_subdirectory": cls.subdirectory,
        }

        if cls.jinja_extensions:
            config["_jinja_extensions"] = cls.jinja_extensions

        for name, field in cls.model_fields.items():
            question: dict[str, Any] = {
                "type": cls._copier_type(field.annotation),
            }

            choices = cls._literal_choices(field.annotation)
            if choices is not None:
                question["choices"] = list(choices)

            if field.default is not PydanticUndefined:
                question["default"] = field.default

            if field.description:
                question["help"] = field.description

            if field.json_schema_extra:
                question.update(field.json_schema_extra)

            config[name] = question

        return config

    @classmethod
    def to_yaml(cls) -> str:
        return yaml.safe_dump(
            cls.to_copier_config(),
            sort_keys=False,
            allow_unicode=True,
        )

    @staticmethod
    def _literal_choices(
        annotation: Any,
    ) -> tuple[Any, ...] | None:
        if get_origin(annotation) is Literal:
            return get_args(annotation)

        return None

    @staticmethod
    def _copier_type(annotation: Any) -> str:
        choices = CopierManifest._literal_choices(annotation)

        if choices:
            annotation = type(choices[0])

        origin = get_origin(annotation)

        if origin is list or origin is dict:
            return "yaml"

        type_mapping = {
            str: "str",
            int: "int",
            float: "float",
            bool: "bool",
            list: "yaml",
            dict: "yaml",
        }

        try:
            return type_mapping[annotation]
        except KeyError as error:
            raise TypeError(
                f"Unsupported Copier question type: {annotation!r}"
            ) from error
