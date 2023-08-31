# Generated by Django 4.2.4 on 2023-08-30 16:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_product_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(default="", max_length=255)),
                ("slug", models.SlugField(blank=True, default="")),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(blank=True, to="products.tag"),
        ),
    ]
