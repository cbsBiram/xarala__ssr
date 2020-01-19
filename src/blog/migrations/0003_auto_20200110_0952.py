# Generated by Django 3.0.1 on 2020-01-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_cloud_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='cloud_image',
        ),
        migrations.AddField(
            model_name='post',
            name='drafted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='image_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
