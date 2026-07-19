import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0008_plan_definition_artifacts")]

    operations = [
        migrations.CreateModel(
            name="PlanArtifactModel",
            fields=[
                ("identifier", models.UUIDField(primary_key=True, serialize=False)),
                ("artifact_id", models.CharField(max_length=255)),
                ("artifact_key", models.CharField(max_length=300, unique=True)),
                ("payload", models.JSONField(default=dict)),
                ("plan_run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="artifacts", to="plans.planrunmodel")),
            ],
        ),
    ]
