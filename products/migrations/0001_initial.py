# Generated by Django 4.2.4 on 2023-10-20 16:53

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("categories", "__first__"),
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
                (
                    "toprated",
                    models.BooleanField(default=False, help_text="1=toprated"),
                ),
                (
                    "bestseller",
                    models.BooleanField(default=False, help_text="1=bestseller"),
                ),
                ("title", models.CharField(max_length=200, verbose_name="title")),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, unique_for_date="publish", verbose_name="slug"
                    ),
                ),
                ("file", models.FileField(blank=True, null=True, upload_to="files")),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, verbose_name="description"
                    ),
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
                ("is_active", models.BooleanField(default=True)),
                ("publish", models.DateTimeField(default=django.utils.timezone.now)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("DF", "Draft"), ("PB", "Published")],
                        default="DF",
                        max_length=2,
                    ),
                ),
                ("download_url", models.CharField(max_length=20, unique=True)),
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
                "ordering": ["-publish"],
            },
        ),
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
        migrations.CreateModel(
            name="SearchTerm",
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
                ("q", models.CharField(max_length=200)),
                ("tracking_id", models.CharField(max_length=255)),
                ("search_date", models.DateTimeField(auto_now_add=True)),
                ("ip_address", models.GenericIPAddressField()),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductView",
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
                ("date", models.DateTimeField(auto_now=True)),
                ("ip_address", models.GenericIPAddressField()),
                ("tracking_id", models.CharField(db_index=True, max_length=255)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
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
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="tag_products", to="products.tag"
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["-publish"], name="products_pr_publish_ffbfbe_idx"
            ),
        ),
    ]
