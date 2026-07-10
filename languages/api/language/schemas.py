from ninja import ModelSchema

from ...models.language import Language


class LanguageOut(ModelSchema):
    class Meta:
        model = Language 
        fields = "__all__"
