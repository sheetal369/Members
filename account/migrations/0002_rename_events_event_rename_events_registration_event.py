# Generated by Django 4.2.6 on 2023-10-15 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Events',
            new_name='Event',
        ),
        migrations.RenameField(
            model_name='registration',
            old_name='Events',
            new_name='Event',
        ),
    ]
