# Generated by Django 2.1.5 on 2019-02-06 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0012_auto_20190206_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='liga_lobby',
            old_name='lug',
            new_name='slug',
        ),
    ]
