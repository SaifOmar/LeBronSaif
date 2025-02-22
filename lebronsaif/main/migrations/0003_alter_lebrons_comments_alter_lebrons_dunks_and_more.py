# Generated by Django 5.0.6 on 2024-05-27 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lebrons',
            name='comments',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='lebrons',
            name='dunks',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='lebrons',
            name='passes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='lebrons',
            name='time_lebroned',
            field=models.DateField(blank=True, null=True),
        ),
    ]
