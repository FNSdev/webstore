# Generated by Django 2.1.7 on 2019-03-13 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190313_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='products',
            field=models.ManyToManyField(through='core.ProductInBasket', to='core.Product'),
        ),
    ]
