# Generated by Django 4.0.1 on 2022-01-19 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_wallet', '0006_alter_mywallet_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='mywallet',
            table='my_wallet',
        ),
    ]
