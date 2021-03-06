# Generated by Django 3.0.2 on 2020-01-20 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='class_groupt',
            new_name='class_group',
        ),
        migrations.AlterField(
            model_name='class',
            name='professors',
            field=models.ManyToManyField(related_name='class_professors', to='User.Professor'),
        ),
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(related_name='class_students', to='User.Student'),
        ),
    ]
