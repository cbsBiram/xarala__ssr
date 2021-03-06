# Generated by Django 3.0.6 on 2020-07-01 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_auto_20200630_0903"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="scoial",
        ),
        migrations.RemoveField(
            model_name="social",
            name="facebook",
        ),
        migrations.RemoveField(
            model_name="social",
            name="github",
        ),
        migrations.RemoveField(
            model_name="social",
            name="instagram",
        ),
        migrations.RemoveField(
            model_name="social",
            name="linkedin",
        ),
        migrations.RemoveField(
            model_name="social",
            name="stackoverflow",
        ),
        migrations.RemoveField(
            model_name="social",
            name="twitter",
        ),
        migrations.RemoveField(
            model_name="social",
            name="website",
        ),
        migrations.RemoveField(
            model_name="social",
            name="whatsapp",
        ),
        migrations.AddField(
            model_name="social",
            name="link",
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="social",
            name="title",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="social",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="socials",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
