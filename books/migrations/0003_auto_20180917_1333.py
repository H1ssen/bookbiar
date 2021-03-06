# Generated by Django 2.0.5 on 2018-09-17 09:03

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20180911_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='authorPic',
            field=models.ImageField(default='/Author/default.png', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\iman\\Desktop\\bookbiar\\site\\prjbrji\\Statics'), upload_to='Authors', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='/Book/default.png', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\iman\\Desktop\\bookbiar\\site\\prjbrji\\Statics'), upload_to='Books', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='publisherPic',
            field=models.ImageField(default='/Publisher/default.png', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\iman\\Desktop\\bookbiar\\site\\prjbrji\\Statics'), upload_to='Publisher', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='translator',
            name='translatorPic',
            field=models.ImageField(default='/Translator/default.png', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\iman\\Desktop\\bookbiar\\site\\prjbrji\\Statics'), upload_to='Translator', verbose_name='تصویر'),
        ),
    ]
