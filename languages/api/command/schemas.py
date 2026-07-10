from ninja import ModelSchema, Schema

from ...models.command import Command


class CommandIn(Schema):
    package_manager_id: str
    result: str
    cmd: str


class CommandPatchIn(Schema):
    package_manager_id: str | None = None
    result: str | None = None
    cmd: str | None = None


class CommandOut(ModelSchema):
    class Meta:
        model = Command
        fields = "__all__"
