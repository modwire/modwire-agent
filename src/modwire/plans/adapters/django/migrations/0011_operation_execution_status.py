from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0010_operation_execution_key")]

    operations = [migrations.AddField(model_name="operationexecutionmodel", name="status", field=models.CharField(default="complete", max_length=32))]
