# Generated by Django 2.1.5 on 2019-02-06 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0009_ligas_endate'),
    ]

    operations = [
        migrations.AddField(
            model_name='players_lobby',
            name='slot',
            field=models.CharField(default=None, max_length=1),
        ),
    ]