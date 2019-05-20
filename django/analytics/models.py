from django.db import models
from django.core.validators import MaxValueValidator

import datetime

from user.models import CustomUser
from core.models import Order


class DataSample(models.Model):
    advertising_costs = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_user_count = models.PositiveIntegerField(default=0)
    new_user_count = models.PositiveIntegerField(default=0)
    orders_count = models.PositiveIntegerField(default=0)
    used_coupone_count = models.PositiveIntegerField(default=0)
    average_discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    profit = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    @staticmethod
    def prepare_sample():
        args = {}

        date = datetime.datetime.now()
        date = date - datetime.timedelta(30)

        args['total_user_count'] = CustomUser.objects.count()
        args['new_user_count'] = CustomUser.objects.filter(date_joined__date__gt=date).count()

        orders = Order.objects.filter(date__date__gt=date)
        args['orders_count'] = orders.count()

        profit = 0
        coupones = 0
        discount = 0
        for order in orders:
            if order.discount != 0:
                coupones += 1
                discount += order.discount
            profit += order.total_price

        if coupones != 0:
            discount /= coupones

        args['used_coupone_count'] = coupones
        args['average_discount'] = discount
        args['profit'] = profit

        return args

    @staticmethod
    def get_data():
        samples = DataSample.objects.all()
        x = []
        y = []
        for sample in samples:
            x_i, y_i = sample.get_sample_data()
            x.append(x_i)
            y.append(y_i)
        return x, y

    def get_sample_data(self):
        x = [
            self.advertising_costs,
            self.total_user_count,
            self.new_user_count,
            self.orders_count,
            self.used_coupone_count,
            self.average_discount,
        ]
        y = self.profit

        return x, y