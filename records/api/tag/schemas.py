from ninja import Schema


class TagIn(Schema):
    name: str
    description: str


class TagPatchIn(Schema):
    name: str
    description: str


class TagOut(Schema):
    slug: str
    name: str
    description: str

    @staticmethod
    def resolve_slug(obj):
        return obj["slug"] if isinstance(obj, dict) else obj.slug
