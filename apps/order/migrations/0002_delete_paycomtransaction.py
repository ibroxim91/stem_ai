# Generated by Django 5.2.1 on 2025-05-23 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaycomTransaction',
        ),
    ]
