# Generated by Django 3.0.5 on 2020-04-16 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_customuser_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
