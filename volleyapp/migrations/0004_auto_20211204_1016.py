# Generated by Django 3.2.9 on 2021-12-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volleyapp', '0003_playerscores_opponent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playername',
            name='name',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='teamname',
            name='team',
            field=models.CharField(max_length=10000),
        ),
    ]
