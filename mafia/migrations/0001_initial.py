# Generated by Django 4.0.6 on 2022-07-14 23:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import django.utils.timezone
import utils.customfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=2500, null=True)),
                ('media', utils.customfields.ContentTypeRestrictedFileField(null=True, upload_to='chat-media/')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='mafia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(code=400, message='can contain only alpha numeric and -, _ and must begin with alphabet', regex='^[a-zA-Z][a-zA-Z0-9_-]+$')])),
                ('verbose_name', models.CharField(max_length=40, null=True)),
                ('icon', utils.customfields.ContentTypeRestrictedFileField(blank=True, null=True, upload_to='mafia-icons/')),
                ('about', models.CharField(blank=True, max_length=350, null=True)),
                ('tag_line', models.CharField(blank=True, max_length=60, null=True)),
                ('color_theme', models.CharField(blank=True, default='#ebade77d', max_length=16, validators=[django.core.validators.RegexValidator(code=400, message='not a valid hex color code', regex='^#+([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$')])),
                ('background_image', utils.customfields.ContentTypeRestrictedFileField(blank=True, null=True, upload_to='mafia_background/')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'mafia',
                'verbose_name_plural': 'mafias',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=250)),
                ('mafia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.mafia')),
            ],
            options={
                'verbose_name': 'mafia rule',
                'verbose_name_plural': 'mafia rules',
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.PositiveSmallIntegerField(choices=[(0, 'heart')])),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mafia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.mafia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='mafia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.mafia'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BanUserFrommafia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mafia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.mafia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='mafia',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='name_unique'),
        ),
    ]