import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Scaffolding",
            fields=[
                (
                    "id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet=None,
                        editable=False,
                        length=22,
                        max_length=22,
                        prefix="",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("language_id", models.CharField(max_length=32)),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField()),
                ("spec", models.JSONField(default=dict)),
            ],
            options={"unique_together": {("language_id", "name")}},
        ),
    ]
