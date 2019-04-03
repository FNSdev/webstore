# Generated by Django 2.1.7 on 2019-03-13 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190312_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInBasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='basket',
            name='products',
        ),
        migrations.AddField(
            model_name='productinbasket',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Basket'),
        ),
        migrations.AddField(
            model_name='productinbasket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product'),
        ),
    ]