from django.db import migrations, models


def split_yaml_types(apps, schema_editor):
    variable = apps.get_model("scaffoldings", "Variable")
    ambiguous = []
    for item in variable.objects.filter(type="yaml").iterator():
        if type(item.default_value) is list:
            item.type = "list"
        elif type(item.default_value) is dict:
            item.type = "dict"
        else:
            ambiguous.append(str(item.id))
            continue
        item.save(update_fields=("type",))
    if ambiguous:
        raise RuntimeError("Cannot infer collection type for YAML variables: " + ", ".join(ambiguous))


class Migration(migrations.Migration):
    dependencies = [("scaffoldings", "0001_initial")]

    operations = [
        migrations.RunPython(split_yaml_types, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="variable",
            name="type",
            field=models.CharField(
                choices=[
                    ("str", "Str"),
                    ("int", "Int"),
                    ("float", "Float"),
                    ("bool", "Bool"),
                    ("list", "List"),
                    ("dict", "Dict"),
                ],
                max_length=8,
            ),
        ),
        migrations.AddField(
            model_name="variable",
            name="required",
            field=models.BooleanField(default=False),
        ),
    ]
