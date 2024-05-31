# Generated by Django 5.0.4 on 2024-04-29 16:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_order_order_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='model_image_1',
            new_name='model_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='model_image_2',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name=datetime.datetime(2024, 4, 29, 18, 56, 56, 589794)),
        ),
    ]