# Generated by Django 2.1.5 on 2019-02-06 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0013_auto_20190206_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players_lobby',
            name='slot',
            field=models.CharField(default=None, max_length=2),
        ),
    ]
