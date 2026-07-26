from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("records", "0001_initial")]

    operations = [migrations.RunSQL("DROP TABLE IF EXISTS tokens_apikey")]
