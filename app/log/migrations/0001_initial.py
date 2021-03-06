# Generated by Django 2.2.1 on 2019-05-08 12:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import log.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('level', models.CharField(choices=[(log.models.LevelChoice('debug'), 'debug'), (log.models.LevelChoice('info'), 'info'), (log.models.LevelChoice('warning'), 'warning'), (log.models.LevelChoice('error'), 'error'), (log.models.LevelChoice('critical'), 'critical')], max_length=20)),
                ('message', models.CharField(max_length=500)),
                ('details', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
