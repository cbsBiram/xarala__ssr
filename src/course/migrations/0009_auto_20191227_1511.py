# Generated by Django 3.0.1 on 2019-12-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0008_remove_lesson_cloudinary_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="chapter",
            name="drafted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="course",
            name="drafted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="lesson",
            name="drafted",
            field=models.BooleanField(default=False),
        ),
    ]
