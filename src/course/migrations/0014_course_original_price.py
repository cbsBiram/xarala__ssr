# Generated by Django 3.0.5 on 2020-05-03 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20200415_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='original_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
    ]