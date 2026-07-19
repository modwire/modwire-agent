from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0003_stage_operations")]

    operations = [migrations.AddField(model_name="planrunmodel", name="revision", field=models.PositiveIntegerField(default=0))]
