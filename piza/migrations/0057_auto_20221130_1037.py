# Generated by Django 3.2 on 2022-11-30 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piza', '0056_alter_deliveryinfo_delivery_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['-order_id'], 'verbose_name': 'Заказы', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['position'], 'verbose_name': 'Продукты', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AddField(
            model_name='deliveryinfo',
            name='courier',
            field=models.CharField(max_length=12, null=True, verbose_name='Курьер'),
        ),
        migrations.AlterField(
            model_name='contact_info',
            name='block',
            field=models.IntegerField(choices=[(0, 'Открыто'), (1, 'Блокирован'), (99, 'Курьер')], default=0, verbose_name='Статус'),
        ),
    ]
