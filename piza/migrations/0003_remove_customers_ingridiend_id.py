# Generated by Django 3.2.7 on 2022-09-14 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piza', '0002_customers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='ingridiend_id',
        ),
    ]
