# Generated by Django 3.2 on 2022-11-17 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0014_alter_authencredentianls_txn_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authencredentianls',
            name='txn_value',
            field=models.IntegerField(default=814980),
        ),
    ]
