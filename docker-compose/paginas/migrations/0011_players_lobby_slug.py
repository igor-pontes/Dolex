# Generated by Django 2.1.5 on 2019-02-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0010_players_lobby_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='players_lobby',
            name='slug',
            field=models.CharField(default=None, max_length=110),
        ),
    ]
