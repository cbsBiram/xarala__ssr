# Generated by Django 3.0.8 on 2020-07-19 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_auto_20200701_1629"),
    ]

    operations = [
        migrations.CreateModel(
            name="Experience",
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
                ("begin_at", models.DateField(blank=True, null=True)),
                ("end_at", models.DateField(blank=True, null=True)),
                ("title", models.CharField(blank=True, max_length=50, null=True)),
                ("Company", models.CharField(blank=True, max_length=50, null=True)),
                ("project_link", models.URLField(blank=True, max_length=50, null=True)),
                ("description", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="customuser",
            name="facebook",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="github",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="linkedin",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="title",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="twitter",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name="Social",
        ),
        migrations.AddField(
            model_name="experience",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="experiences",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
