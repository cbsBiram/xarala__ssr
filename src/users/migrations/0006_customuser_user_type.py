# Generated by Django 2.2.7 on 2019-12-15 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_auto_20190922_1812"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("ST", "Student"),
                    ("TC", "Teacher"),
                    ("MT", "Mentor"),
                    ("WT", "Writer"),
                ],
                default="ST",
                max_length=10,
            ),
        ),
    ]
