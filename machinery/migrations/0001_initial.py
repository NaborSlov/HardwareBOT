# Generated by Django 4.2.3 on 2023-07-27 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Industrial_unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название установки')),
            ],
            options={
                'verbose_name': 'Установка',
                'verbose_name_plural': 'Установки',
            },
        ),
        migrations.CreateModel(
            name='Machine_node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название узла')),
                ('industial_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industial_units', to='machinery.industrial_unit', verbose_name='Установка')),
            ],
            options={
                'verbose_name': 'Узел установки',
                'verbose_name_plural': 'Узлы установки',
            },
        ),
    ]