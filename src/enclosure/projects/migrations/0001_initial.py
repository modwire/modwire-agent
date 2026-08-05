import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("root", models.CharField(max_length=1024, unique=True)),
                ("architecture_root", models.CharField(max_length=1024)),
                ("language_id", models.CharField(max_length=32)),
                ("language_version", models.CharField(max_length=32)),
                ("package_manager_id", models.CharField(max_length=32)),
                ("boundaries_yaml", models.TextField()),
                ("shape_yaml", models.TextField()),
                ("scaffolding_id", models.CharField(max_length=22)),
            ],
        ),
        migrations.CreateModel(
            name="ProjectRecord",
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
                ("record_id", models.CharField(max_length=22)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="record_bindings",
                        to="projects.project",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="projectrecord",
            constraint=models.UniqueConstraint(
                fields=("project", "record_id"),
                name="projects_project_record_unique",
            ),
        ),
    ]
