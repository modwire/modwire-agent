from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0007_gate_satisfaction_key")]

    operations = [migrations.AddField(model_name="plandefinitionmodel", name="artifacts", field=models.JSONField(default=list))]
