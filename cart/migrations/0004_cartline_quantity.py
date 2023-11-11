# Generated by Django 4.2.4 on 2023-10-27 17:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0003_remove_cartline_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartline",
            name="quantity",
            field=models.PositiveIntegerField(
                default=1, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
    ]