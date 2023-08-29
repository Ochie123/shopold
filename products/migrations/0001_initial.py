# Generated by Django 4.2.4 on 2023-08-27 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=None, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="title")),
                ("slug", models.SlugField(max_length=200, verbose_name="slug")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=8,
                        null=True,
                        verbose_name="price ($)",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="category_products",
                        to="categories.category",
                        verbose_name="Categories",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="product-images", verbose_name="image"),
                ),
                (
                    "thumbnail",
                    models.ImageField(null=True, upload_to="product-thumbnails"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
                "ordering": ("order",),
                "abstract": False,
            },
        ),
    ]