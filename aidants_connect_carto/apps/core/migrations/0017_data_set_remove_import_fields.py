# Generated by Django 3.0.5 on 2020-11-18 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_auto_20201116_2125"),
    ]

    operations = [
        migrations.RemoveField(model_name="dataset", name="import_comment",),
        migrations.RemoveField(model_name="dataset", name="import_config",),
    ]
