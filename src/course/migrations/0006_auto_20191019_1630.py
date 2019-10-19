# Generated by Django 2.2.6 on 2019-10-19 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20191018_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_chapters', to='course.Course'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_lessons', to='course.Chapter'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='platform',
            field=models.CharField(choices=[('Youtube', 'Youtube'), ('Vimeo', 'Vimeo'), ('Wista', 'Wista'), ('Custom', 'Custom'), ('CloudiNary', 'CloudiNary')], default='Youtube', max_length=50),
        ),
    ]
