# Generated by Django 3.0.8 on 2020-07-20 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20200719_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_at', models.DateField(blank=True, null=True)),
                ('end_at', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('school', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='educations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]