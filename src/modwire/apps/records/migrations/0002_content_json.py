from django.db import migrations, models

from modwire.apps.records.models.content import Content as CurrentContent


def encode_content(role, value):
    return value.splitlines() if role == CurrentContent.Role.LIST else value


def decode_content(value):
    return "\n".join(value) if isinstance(value, list) else value


def to_json_content(apps, schema_editor):
    Content = apps.get_model("records", "Content")
    for block in Content.objects.all().iterator():
        block.content_data = encode_content(block.role, block.content)
        block.save(update_fields=["content_data"])


def to_text_content(apps, schema_editor):
    Content = apps.get_model("records", "Content")
    for block in Content.objects.all().iterator():
        value = block.content_data
        block.content = decode_content(value)
        block.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [("records", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="content",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="content",
            name="content_data",
            field=models.JSONField(null=True),
        ),
        migrations.RunPython(to_json_content, to_text_content),
        migrations.RemoveField(model_name="content", name="content"),
        migrations.RenameField(model_name="content", old_name="content_data", new_name="content"),
        migrations.AlterField(model_name="content", name="content", field=models.JSONField()),
    ]
