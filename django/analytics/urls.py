from django.urls import path

from analytics.views import *


app_name = 'analytics'
urlpatterns = [
    path('', AnalyticsView.as_view(), name='analytics'),
    path('add-data-sample/', AddDataSampleView.as_view(), name='add-data-sample'),
    path('train-model/', TrainModelView.as_view(), name='train-model'),
    path('predict-profit/', PredictProfitView.as_view(), name='predict-profit')
]