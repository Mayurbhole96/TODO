# Generated by Django 4.2 on 2023-09-02 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'verbose_name_plural': 'Todo List'},
        ),
        migrations.AddField(
            model_name='todo',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AddField(
            model_name='todo',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Is Deleted'),
        ),
        migrations.AlterModelTable(
            name='todo',
            table='table_todo',
        ),
    ]