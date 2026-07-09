from ninja import Schema


class SectionIn(Schema):
    title: str
    description: str
    tag_slugs: list[str]


class SectionPatchIn(Schema):
    title: str
    description: str
    tag_slugs: list[str]


class SectionOut(Schema):
    slug: str
    title: str
    description: str
    tag_slugs: list[str]

    @staticmethod
    def resolve_tag_slugs(obj):
        if isinstance(obj, dict):
            return obj["tag_slugs"]
        return list(obj.tags.order_by("slug").values_list("slug", flat=True))
