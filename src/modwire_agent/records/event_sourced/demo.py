from eventsourcing.system import SingleThreadedRunner

from .application import RecordsApplication
from .projections import RecordsProjection
from .system import records_system


def run() -> dict[str, object]:
    runner = SingleThreadedRunner(records_system, env={"PERSISTENCE_MODULE": "eventsourcing.popo"})
    runner.start()
    try:
        records = runner.get(RecordsApplication)
        section = records.create_section("Architecture", ["rule"])
        tag = records.create_tag("testing")
        record = records.create_record(section.id, "HTTP contract", "rule")
        records.assign_tags(record.id, [tag.id])
        records.replace_content(record.id, "## Rules\n\nUse HTTP.\n\n## Verification\n\nRun tests.", "agent-1", "agent")
        records.publish_record(record.id)
        return runner.get(RecordsProjection).catalogue().events
    finally:
        runner.stop()
