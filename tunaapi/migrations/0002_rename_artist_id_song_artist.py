# Generated by Django 4.1.3 on 2023-12-06 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tunaapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='artist_id',
            new_name='artist',
        ),
    ]
