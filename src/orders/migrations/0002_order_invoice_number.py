# Generated by Django 3.1.5 on 2021-01-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
