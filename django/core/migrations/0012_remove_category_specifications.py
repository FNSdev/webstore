# Generated by Django 2.1.7 on 2019-03-27 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_category_specifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='specifications',
        ),
    ]