# Generated by Django 3.1.4 on 2020-12-23 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_app', '0006_auto_20201222_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneytransfer',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
