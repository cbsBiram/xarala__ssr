# Generated by Django 2.2.5 on 2019-09-10 13:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subscribe",
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
                ("email_id", models.EmailField(blank=True, max_length=254, null=True)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
