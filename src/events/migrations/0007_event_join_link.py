# Generated by Django 2.2.5 on 2019-09-28 19:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20190922_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='join_link',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]