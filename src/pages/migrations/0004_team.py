# Generated by Django 3.0.6 on 2020-07-16 10:16

from django.db import migrations, models
import xarala.utils


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_contact"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
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
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                ("email", models.CharField(max_length=150)),
                ("phone", models.CharField(max_length=150)),
                ("profession", models.CharField(max_length=150)),
                (
                    "profile",
                    models.ImageField(
                        blank=True, null=True, upload_to=xarala.utils.upload_image_path
                    ),
                ),
                ("bio", models.TextField()),
                ("website", models.URLField(blank=True, max_length=150, null=True)),
                ("facebook", models.URLField(blank=True, max_length=150, null=True)),
                ("twitter", models.URLField(blank=True, max_length=150, null=True)),
            ],
        ),
    ]
