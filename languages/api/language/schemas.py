from ninja import ModelSchema, Schema

from ...models.language import Language 


class LanguageIn(Schema):
    name: str


class LanguagePatchIn(Schema):
    name: str


class LanguageOut(ModelSchema):
    class Meta:
        model = Language 
        fields = "__all__"
