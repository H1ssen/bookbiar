# Generated by Django 2.0.5 on 2018-09-11 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='typeId',
            new_name='mainCat',
        ),
    ]