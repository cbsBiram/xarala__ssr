# Generated by Django 2.2.5 on 2019-09-22 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_customuser_bio"),
    ]

    operations = [
        migrations.CreateModel(
            name="Designation",
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
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="customuser",
            name="designation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.Designation",
            ),
        ),
    ]
