from ninja import ModelSchema

from shared.api.types import ShortUUID

from ...models.command import Command, CommandResult


class CommandOut(ModelSchema):
    id: ShortUUID
    package_manager: ShortUUID
    result: CommandResult

    @staticmethod
    def resolve_package_manager(obj):
        return obj.package_manager_id

    class Meta:
        model = Command
        fields = "__all__"
