from ninja import ModelSchema

from ...models.command import Command


class CommandOut(ModelSchema):
    class Meta:
        model = Command
        fields = "__all__"
