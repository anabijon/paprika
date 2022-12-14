# Generated by Django 3.2 on 2022-09-21 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piza', '0034_auto_20220921_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitem',
            name='volume',
        ),
        migrations.RemoveField(
            model_name='products',
            name='price',
        ),
        migrations.AlterField(
            model_name='productitem',
            name='volume_name',
            field=models.IntegerField(choices=[(1, '33см'), (2, '40см'), (3, '1.5л'), (4, '1.0л'), (5, '0.5л'), (6, '1.75л'), (7, '0.33л')], verbose_name='Объем/Размер'),
        ),
    ]
