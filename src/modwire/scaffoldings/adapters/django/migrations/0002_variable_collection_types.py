from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("scaffoldings", "0001_initial")]

    operations = [
        migrations.RunSQL(
            "UPDATE scaffoldings_variable SET type = CASE jsonb_typeof(default_value) WHEN 'array' THEN 'list' WHEN 'object' THEN 'dict' ELSE type END WHERE type = 'yaml'",
            migrations.RunSQL.noop,
        ),
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
