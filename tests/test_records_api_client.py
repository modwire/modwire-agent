import pytest
from oa.api.records import create_record, get_record, list_records, search_records
from oa.api.sections import create_section, list_sections
from oa.api.tags import create_tag, list_tags
from oa.models.content_in import ContentIn
from oa.models.content_in_role import ContentInRole
from oa.models.record_content_in_metadata import RecordContentInMetadata
from oa.models.record_in import RecordIn
from oa.models.record_search_result_out import RecordSearchResultOut
from oa.models.search_in import SearchIn
from oa.models.search_in_mode import SearchInMode
from oa.models.search_in_target import SearchInTarget
from oa.models.section_in import SectionIn
from oa.models.tag_in import TagIn


@pytest.mark.django_db(transaction=True)
def test_records_api_roundtrip_and_vector_search_use_generated_client(api_client):
    tag = create_tag.sync(
        client=api_client,
        body=TagIn(name="Architecture", description="Architecture knowledge."),
    )
    assert tag is not None
    assert tag.slug == "architecture"

    section = create_section.sync(
        client=api_client,
        body=SectionIn(
            title="Software Architecture",
            description="Architecture records and references.",
            tag_slugs=[tag.slug],
        ),
    )
    assert section is not None
    assert section.slug == "software-architecture"
    assert section.tag_slugs == [tag.slug]

    metadata = RecordContentInMetadata()
    metadata["source"] = "functional-test"
    record = create_record.sync(
        client=api_client,
        body=RecordIn(
            section_slug=section.slug,
            title="Architecture Decision Record",
            description="A short note about documenting architectural decisions.",
            sources=["https://example.test/adr"],
            tag_slugs=[tag.slug],
            content=[
                ContentIn(
                    role=ContentInRole.PARAGRAPH,
                    content="Architecture decision records capture context, decision, and consequences.",
                    language="text",
                    metadata=metadata,
                )
            ],
        ),
    )
    assert record is not None
    assert record.slug == "software-architecture/architecture-decision-record"
    assert record.tag_slugs == [tag.slug]
    assert record.content[0].metadata["source"] == "functional-test"

    tags = list_tags.sync(client=api_client)
    assert tags is not None
    assert [item.slug for item in tags] == [tag.slug]

    sections = list_sections.sync(client=api_client, limit=10, offset=0, tag=[tag.slug])
    assert sections is not None
    assert [item.slug for item in sections] == [section.slug]

    records = list_records.sync(
        client=api_client,
        limit=10,
        offset=0,
        section_slugs=[section.slug],
        tag=[tag.slug],
    )
    assert records is not None
    assert [item.slug for item in records] == [record.slug]

    fetched = get_record.sync(client=api_client, record_slug=record.slug)
    assert fetched is not None
    assert fetched.sources == ["https://example.test/adr"]

    results = search_records.sync(
        client=api_client,
        body=SearchIn(
            query="architecture decision context consequence",
            mode=SearchInMode.VECTOR,
            target=SearchInTarget.RECORDS,
            limit=5,
            offset=0,
            section_slugs=[section.slug],
            tag_slugs=[tag.slug],
        ),
    )
    assert results is not None
    assert results.results
    assert isinstance(results.results[0], RecordSearchResultOut)
    assert results.results[0].slug == record.slug
