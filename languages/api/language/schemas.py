from ninja import ModelSchema

from shared.api_types import ShortUUID

from ...models.language import Language


class LanguageOut(ModelSchema):
    id: ShortUUID

    class Meta:
        model = Language
        fields = "__all__"
