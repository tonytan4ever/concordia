# Generated by Django 2.0.7 on 2018-07-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("concordia", "0009_auto_20180730_2017")]

    operations = [
        migrations.AlterField(
            model_name="pageinuse", name="updated_on", field=models.DateTimeField()
        )
    ]
