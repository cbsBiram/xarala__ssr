# Generated by Django 3.0.8 on 2020-07-20 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_lesson_lecture_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]