# Generated by Django 3.0.5 on 2020-04-14 12:41

from django.db import migrations, models
import xarala.utils


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Carousel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("link_to", models.URLField()),
                ("link_text", models.CharField(max_length=50)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=xarala.utils.upload_image_path
                    ),
                ),
                ("active", models.BooleanField(default=False)),
            ],
        ),
    ]
