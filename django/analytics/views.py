from django.views import View
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect, reverse
from django.http import JsonResponse

from analytics.models import DataSample
from analytics.forms import DataSampleForm, PredictForm
from analytics.analytics import Model

class AnalyticsView(TemplateView):
    template_name = 'analytics/analytics.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = DataSampleForm()
        ctx['prepopulated_form'] = DataSampleForm(initial=DataSample.make_sample())
        ctx['predict_form'] = PredictForm()
        return ctx


class AddDataSampleView(CreateView):
    form_class = DataSampleForm

    def get_success_url(self):
        return reverse('analytics:analytics')

    def render_to_response(self, context, **response_kwargs):
        return redirect(to=self.get_success_url())


class TrainModelView(View):
    def get(self, request):
        x, y = DataSample.get_data()
        model = Model()
        model.train(x, y)
        return JsonResponse({'status': 'ok', 'coefficients': list(model.get_coefficients())})


class PredictProfitView(View):
    def get(self, request):
        args = request.GET
        print(args)
        x = [
            float(args['advertising_costs']),
            int(args['total_user_count']),
            int(args['new_user_count']),
            int(args['used_coupone_count']),
            float(args['average_discount']),
        ]
        print(x)
        profit = Model().predict(x)
        print(args)
        print(profit)
        return JsonResponse({'profit': profit})