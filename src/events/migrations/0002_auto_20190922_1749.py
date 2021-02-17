# Generated by Django 2.2.5 on 2019-09-22 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="place",
            new_name="location",
        ),
        migrations.AddField(
            model_name="event",
            name="country",
            field=models.CharField(max_length=240, null=True),
        ),
    ]
