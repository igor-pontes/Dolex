# Generated by Django 2.1.5 on 2019-02-06 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0004_players_lobby'),
    ]

    operations = [
        migrations.AddField(
            model_name='liga_lobby',
            name='slots',
            field=models.BigIntegerField(default=10),
        ),
    ]
