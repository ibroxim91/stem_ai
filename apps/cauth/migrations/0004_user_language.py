# Generated by Django 5.2.1 on 2025-05-16 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cauth', '0003_alter_user_tariff'),
        ('main', '0004_alter_projectcategorytranslation_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.language'),
        ),
    ]
