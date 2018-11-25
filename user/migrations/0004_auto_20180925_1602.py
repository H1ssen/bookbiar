# Generated by Django 2.0.5 on 2018-09-25 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20180925_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carditem',
            name='allBookDiscountPrice',
        ),
        migrations.RemoveField(
            model_name='carditem',
            name='allBookPayedPrice',
        ),
        migrations.AddField(
            model_name='card',
            name='discountPrice',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='card',
            name='payedPrice',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='card',
            name='discountCodePrice',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=6),
        ),
    ]