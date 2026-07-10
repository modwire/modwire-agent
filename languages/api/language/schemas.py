from ninja import ModelSchema, Schema

from ...models.language import Language


class LanguageIn(Schema):
    name: str
    executable: str
    stable_version: str


class LanguagePatchIn(Schema):
    name: str | None = None
    executable: str | None = None
    stable_version: str | None = None


class LanguageOut(ModelSchema):
    class Meta:
        model = Language 
        fields = "__all__"
