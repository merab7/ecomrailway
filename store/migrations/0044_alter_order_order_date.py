# Generated by Django 5.0.2 on 2024-05-15 16:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0043_alter_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name=datetime.datetime(2024, 5, 15, 18, 12, 29, 473966)),
        ),
    ]
