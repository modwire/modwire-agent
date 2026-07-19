from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("plans", "0005_plan_definition_name_version")]

    operations = [
        migrations.AddField(model_name="plandefinitionmodel", name="publication_key", field=models.CharField(max_length=300, null=True)),
        migrations.RunSQL(
            sql="UPDATE plans_plandefinitionmodel SET publication_key = name || ':' || version",
            reverse_sql="UPDATE plans_plandefinitionmodel SET publication_key = NULL",
        ),
        migrations.AlterField(model_name="plandefinitionmodel", name="publication_key", field=models.CharField(max_length=300, unique=True)),
        migrations.RemoveConstraint(model_name="plandefinitionmodel", name="plans_definition_name_version"),
    ]
