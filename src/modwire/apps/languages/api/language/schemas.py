from ninja import ModelSchema

from modwire.shared.api.types import ShortUUID

from ...models.language import Language


class LanguageOut(ModelSchema):
    id: ShortUUID

    class Meta:
        model = Language
        fields = "__all__"
