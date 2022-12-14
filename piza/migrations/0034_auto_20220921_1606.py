# Generated by Django 3.2.7 on 2022-09-21 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piza', '0033_remove_productitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='volume_name',
            field=models.CharField(max_length=12, null=True, verbose_name='Объем/Размер'),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
    ]
