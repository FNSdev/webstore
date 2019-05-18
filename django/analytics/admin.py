from django.contrib import admin

from analytics.models import *
from analytics.forms import DataSampleForm

class DataSampleAdmin(admin.ModelAdmin):
    form = DataSampleForm
    list_display = ['profit', 'advertising_costs', 'total_user_count', 'new_user_count', 'used_coupone_count', 'average_discount']

admin.site.register(DataSample, DataSampleAdmin)
