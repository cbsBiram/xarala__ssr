# Generated by Django 3.0.5 on 2020-05-04 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0016_auto_20200504_0056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='is_free',
            new_name='is_tutorial',
        ),
    ]
