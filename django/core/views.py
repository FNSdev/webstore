from django.views.generic import TemplateView, ListView
from django.views import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category, Product


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
        #ctx['filter_form']
        ctx['paginate_by'] = self.paginate_by
        return ctx

    def get_queryset(self):
        category_slug = self.kwargs['category']
        cat = get_object_or_404(Category, slug__iexact=category_slug)
        return cat.products.all()

    def get(self, request, *args, **kwargs):
        if request.GET.get('paginate_by'):
            self.paginate_by = request.GET['paginate_by']
        return super().get(request, *args, **kwargs)