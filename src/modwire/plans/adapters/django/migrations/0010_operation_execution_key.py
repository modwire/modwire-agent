from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0009_plan_artifact")]

    operations = [
        migrations.AddField(model_name="operationexecutionmodel", name="execution_key", field=models.CharField(max_length=300, null=True)),
        migrations.RunSQL(
            sql="UPDATE plans_operationexecutionmodel SET execution_key = plan_run_id || ':' || operation_id",
            reverse_sql="UPDATE plans_operationexecutionmodel SET execution_key = NULL",
        ),
        migrations.AlterField(model_name="operationexecutionmodel", name="execution_key", field=models.CharField(max_length=300, unique=True)),
    ]
