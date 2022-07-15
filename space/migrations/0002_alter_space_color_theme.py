# Generated by Django 4.0.6 on 2022-07-15 00:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='color_theme',
            field=models.CharField(blank=True, default='#f5d1e0', max_length=16, validators=[django.core.validators.RegexValidator(code=400, message='not a valid hex color code', regex='^#+([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$')]),
        ),
    ]
