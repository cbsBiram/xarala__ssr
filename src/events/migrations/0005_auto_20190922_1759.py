# Generated by Django 2.2.5 on 2019-09-22 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_event_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="short_description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
