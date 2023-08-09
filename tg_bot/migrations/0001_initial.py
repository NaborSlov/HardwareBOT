# Generated by Django 4.2.3 on 2023-08-08 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('login', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='login name')),
                ('password', models.CharField(max_length=255, verbose_name='password')),
                ('tg_login', models.BigIntegerField(blank=True, db_index=True, unique=True, verbose_name='login_tg_bot')),
            ],
            options={
                'verbose_name': 'Tg_user',
                'verbose_name_plural': 'Tg_users',
            },
        ),
    ]
