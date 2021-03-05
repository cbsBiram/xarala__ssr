# Generated by Django 3.1.6 on 2021-03-05 13:06

from django.db import migrations, models
import xarala.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0028_course_submitted'),
        ('blog', '0008_auto_20210303_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=xarala.utils.upload_image_path)),
                ('description', models.TextField()),
                ('path_type', models.CharField(choices=[('Django', 'Django'), ('React', 'React'), ('Python', 'Python')], max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ManyToManyField(blank=True, to='course.Course')),
                ('tutorials', models.ManyToManyField(blank=True, to='blog.Post')),
            ],
        ),
    ]
