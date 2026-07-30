from modwire_hex.django import DjangoRequest
from ninja import Status
from ninja_extra import ControllerBase, api_controller, route

from ..services import RecordsService
from . import schemas


@api_controller("/records/tags", tags=["Record tags"])
class TagsController(ControllerBase):
    @route.post("", response={201: schemas.Tag}, operation_id="create_record_tag")
    def create(self, request, body: schemas.TagInput):
        tag = DjangoRequest.resolve(request, RecordsService).create_tag(body.model_dump(mode="json"))
        return Status(201, tag)

    @route.get("", response=list[schemas.Tag], operation_id="find_record_tags")
    def find_all(self, request):
        return DjangoRequest.resolve(request, RecordsService).find_all_tags()

    @route.get("/{tag_id}", response=schemas.Tag, operation_id="get_record_tag")
    def get(self, request, tag_id: str):
        return DjangoRequest.resolve(request, RecordsService).get_tag(tag_id)

    @route.put("/{tag_id}", response=schemas.Tag, operation_id="update_record_tag")
    def update(self, request, tag_id: str, body: schemas.TagInput):
        return DjangoRequest.resolve(request, RecordsService).update_tag(tag_id, body.model_dump(mode="json"))

    @route.delete("/{tag_id}", response={204: None}, operation_id="delete_record_tag")
    def delete(self, request, tag_id: str):
        DjangoRequest.resolve(request, RecordsService).delete_tag(tag_id)
        return Status(204, None)


@api_controller("/records", tags=["Records"])
class RecordsController(ControllerBase):
    @route.post("", response={201: schemas.Record}, operation_id="create_record")
    def create(self, request, body: schemas.RecordInput):
        record = DjangoRequest.resolve(request, RecordsService).create_record(body.model_dump(mode="json"))
        return Status(201, record)

    @route.get("", response=list[schemas.RecordSummary], operation_id="find_records")
    def find_all(self, request):
        return DjangoRequest.resolve(request, RecordsService).find_all_records()

    @route.post("/search", response=list[schemas.Record], operation_id="search_records")
    def search(self, request, body: schemas.SearchInput):
        return DjangoRequest.resolve(request, RecordsService).search_records(body.query, body.limit)

    @route.post("/categories", response={201: schemas.Category}, operation_id="create_record_category")
    def create_category(self, request, body: schemas.CategoryInput):
        category = DjangoRequest.resolve(request, RecordsService).create_category(body.model_dump(mode="json"))
        return Status(201, category)

    @route.get("/categories", response=list[schemas.Category], operation_id="find_record_categories")
    def find_all_categories(self, request):
        return DjangoRequest.resolve(request, RecordsService).find_all_categories()

    @route.get("/categories/{category_id}", response=schemas.Category, operation_id="get_record_category")
    def get_category(self, request, category_id: str):
        return DjangoRequest.resolve(request, RecordsService).get_category(category_id)

    @route.put("/categories/{category_id}", response=schemas.Category, operation_id="update_record_category")
    def update_category(self, request, category_id: str, body: schemas.CategoryInput):
        return DjangoRequest.resolve(request, RecordsService).update_category(
            category_id,
            body.model_dump(mode="json"),
        )

    @route.delete("/categories/{category_id}", response={204: None}, operation_id="delete_record_category")
    def delete_category(self, request, category_id: str):
        DjangoRequest.resolve(request, RecordsService).delete_category(category_id)
        return Status(204, None)

    @route.get("/{record_id}", response=schemas.Record, operation_id="get_record")
    def get(self, request, record_id: str):
        return DjangoRequest.resolve(request, RecordsService).get_record(record_id)

    @route.put("/{record_id}", response=schemas.Record, operation_id="update_record")
    def update(self, request, record_id: str, body: schemas.RecordInput):
        return DjangoRequest.resolve(request, RecordsService).update_record(record_id, body.model_dump(mode="json"))

    @route.delete("/{record_id}", response={204: None}, operation_id="delete_record")
    def delete(self, request, record_id: str):
        DjangoRequest.resolve(request, RecordsService).delete_record(record_id)
        return Status(204, None)
