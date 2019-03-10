from django.views.generic import TemplateView, ListView
from django.views import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category, Product
from .forms import SmartphoneFilterForm


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductsView(ListView):
    paginate_by = 10
    model = Product
    template_name = 'core/products.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)       
        ctx['paginate_by'] = self.paginate_by

        args = self.request.GET.dict()
        form = SmartphoneFilterForm(initial=args)

        ctx['filter_form'] = form
        return ctx

    def get_queryset(self):
        category_slug = self.kwargs['category']
        cat = get_object_or_404(Category, slug__iexact=category_slug)

        query_dict = self.request.GET
        args = query_dict.dict()
        order_by = False
                
        if args.get('paginate_by'):
            del args['paginate_by']
        if args.get('order_by'):
            order_by = args['order_by']
            del args['order_by']
        if args.get('page'):
            del args['page']

        for k in [k for k, v in args.items() if not v]:
            del args[k]

        qs = cat.products.filter(specifications__contains=args)
        if order_by:
            qs = qs.order_by(order_by)

        return qs

    def get(self, request, *args, **kwargs):
        if request.GET.get('paginate_by'):
            self.paginate_by = request.GET['paginate_by']
        return super().get(request, *args, **kwargs)