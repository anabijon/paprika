# Generated by Django 3.2.7 on 2022-09-21 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piza', '0032_auto_20220921_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitem',
            name='quantity',
        ),
    ]
