from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0004_plan_run_revision")]

    operations = [migrations.AddConstraint(model_name="plandefinitionmodel", constraint=models.UniqueConstraint(fields=("name", "version"), name="plans_definition_name_version"))]
