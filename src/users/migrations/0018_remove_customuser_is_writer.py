# Generated by Django 3.1.6 on 2021-02-16 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210115_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_writer',
        ),
    ]