from django.views import View
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin

from analytics.models import DataSample
from analytics.forms import DataSampleForm, PredictForm
from analytics.analytics import train_profit, predict_profit, get_coefficients


class AnalyticsView(PermissionRequiredMixin, TemplateView):
    template_name = 'analytics/analytics.html'
    login_url = '/user/login'
    permission_required = ('data_sample.can_add')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = DataSampleForm()
        ctx['prepopulated_form'] = DataSampleForm(initial=DataSample.prepare_sample())
        ctx['predict_form'] = PredictForm()
        return ctx


class AddDataSampleView(PermissionRequiredMixin, CreateView):
    form_class = DataSampleForm
    login_url = '/user/login'
    permission_required = ('data_sample.can_add')

    def get_success_url(self):
        return reverse('analytics:analytics')

    def render_to_response(self, context, **response_kwargs):
        return redirect(to=self.get_success_url())


class TrainModelView(PermissionRequiredMixin, View):
    login_url = '/user/login'
    permission_required = ('data_sample.can_add')

    def get(self, request):
        x, y = DataSample.get_data()
        train_profit(x, y)
        return JsonResponse({'status': 'ok', 'coefficients': list(get_coefficients())})


class PredictProfitView(PermissionRequiredMixin, View):
    login_url = '/user/login'
    permission_required = ('data_sample.can_add')

    def get(self, request):
        args = request.GET
        x = [
            float(args['advertising_costs']),
            int(args['total_user_count']),
            int(args['new_user_count']),
            int(args['orders_count']),
            int(args['used_coupone_count']),
            float(args['average_discount']),
        ]
        profit = predict_profit(x)
        return JsonResponse({'profit': profit})
