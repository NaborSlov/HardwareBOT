# Generated by Django 4.2.3 on 2023-08-08 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0003_alter_tguser_tg_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='tg_login',
            field=models.CharField(blank=True, max_length=255, verbose_name='Телеграм логин'),
        ),
    ]