# Generated by Django 5.0.4 on 2024-05-28 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_profile_old_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
