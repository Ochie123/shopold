# Generated by Django 4.2.4 on 2023-10-27 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_productview_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productview",
            name="location",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
