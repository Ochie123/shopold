# Generated by Django 4.2.4 on 2023-08-27 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_searchterm_productview"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
