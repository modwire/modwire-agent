from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0006_plan_definition_publication_key")]

    operations = [
        migrations.AddField(model_name="gatesatisfactionmodel", name="satisfaction_key", field=models.CharField(max_length=300, null=True)),
        migrations.RunSQL(
            sql="UPDATE plans_gatesatisfactionmodel SET satisfaction_key = plan_run_id || ':' || gate_id",
            reverse_sql="UPDATE plans_gatesatisfactionmodel SET satisfaction_key = NULL",
        ),
        migrations.AlterField(model_name="gatesatisfactionmodel", name="satisfaction_key", field=models.CharField(max_length=300, unique=True)),
    ]
