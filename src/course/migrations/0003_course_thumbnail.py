# Generated by Django 2.2.5 on 2019-09-14 00:06

from django.db import migrations, models
import xarala.utils


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20190914_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=xarala.utils.upload_image_path),
        ),
    ]
