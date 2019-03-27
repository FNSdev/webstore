from django.views.generic import DetailView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


from .models import Category, Product, Announcement, ProductInBasket
from user.models import CustomUser
from .forms import SmartphoneFilterForm

import decimal
import ast


class IndexView(ListView):
    template_name = "core/index.html"
    model = Announcement
    paginate_by = 3

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


class AnnouncementDetailView(DetailView):
    model = Announcement


class ProductDetailView(DetailView):
    model = Product

    def get(self, *args, **kwargs):
        obj = self.get_object()
        obj.view_count += 1
        obj.save()
        return super().get(*args, **kwargs)
    

class AddToBasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def post(self, request, *args, **kwargs):
        product_id = request.POST['id']
        count = request.POST['count']
        user = request.user 

        product = Product.objects.filter(id__iexact=product_id).first()

        basket = user.basket 
        basket.total_count += 1
        basket.save()

        ProductInBasket.objects.create(product=product, basket=user.basket, count=count)

        return JsonResponse({'count': basket.total_count})


class UpdateBasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def post(self, request, *args, **kwargs):
        basket = request.user.basket 
        pairs = request.POST['pairs']

        pairs = ast.literal_eval(pairs)
        
        for key, value in pairs.items():
            product_in_basket = ProductInBasket.objects.get(id__iexact=key)
            product_in_basket.count = int(value)
            product_in_basket.save()

        print('updating basket')

        return JsonResponse({})

    
class RemoveFromBasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def post(self, request, *args, **kwargs):
        product_id = request.POST['id']
        basket = request.user.basket 

        product_in_basket = ProductInBasket.objects.get(id__iexact=product_id)

        basket.total_count -= 1
        basket.save()

        product_in_basket.delete()
        total = basket.get_total_price()

        return JsonResponse({'total': total, 'count': basket.total_count})


class BasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def get(self, request, *args, **kwargs):
        basket = request.user.basket
        products = ProductInBasket.objects.filter(basket__id=basket.id)

        return render(request, 'core/basket.html', {'products': products, 'total': basket.get_total_price()})


class ConfirmOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        basket = request.user.basket
        products_in_basket = ProductInBasket.objects.filter(basket__id = basket.id)

        for p in products_in_basket:
            #print(f'{p.product.name} : {p.count}')
            print(p)

        return render(request, 'core/confirm-order.html', {'products_in_basket' : products_in_basket})