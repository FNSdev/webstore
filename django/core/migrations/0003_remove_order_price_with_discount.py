# Generated by Django 2.1.7 on 2019-05-17 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190415_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price_with_discount',
        ),
    ]
