# Generated by Django 3.0.2 on 2020-01-20 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20200120_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='class_group',
        ),
        migrations.AddField(
            model_name='test',
            name='class_group',
            field=models.ManyToManyField(to='User.Class'),
        ),
    ]
