# Generated by Django 5.2.1 on 2025-05-12 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=10),
        ),
    ]
