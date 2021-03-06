from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseNotFound
from django.core.exceptions import PermissionDenied

from core.models import Category, Product, Announcement, ProductInBasket, Order, ProductInOrder, Review, Coupone
from core.models import MAX_PRODUCT_IN_BASKET_OR_ORDER_COUNT
from core.forms import GENERATED_FORMS, ReviewForm, OrderForm

import ast
import re
import logging

logger = logging.getLogger('django.bad_request_args')

UUID4_PATTERN = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'


class IndexView(ListView):
    template_name = "core/index.html"
    model = Announcement
    paginate_by = 3

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class SearchView(ListView):
    paginate_by = 10
    model = Product
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        ctx['search'] = search if search is not None else ''
        ctx['categories'] = Category.objects.all()
        return ctx

    def get_queryset(self):
        name = self.request.GET.get('search')
        if name is None:
            logger.warning('search, name = None')
            qs = Product.objects.all()
        else:
            qs = Product.objects.filter(name__icontains=name)
        return qs


class ProductsView(ListView):
    paginate_by = 10
    model = Product
    template_name = 'core/products.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['paginate_by'] = self.paginate_by

        args = self.request.GET.dict()
        category_slug = self.kwargs['category']

        form = GENERATED_FORMS.get(category_slug)
        if form:
            ctx['filter_form'] = form(initial=args)
        ctx['max_cnt'] = MAX_PRODUCT_IN_BASKET_OR_ORDER_COUNT
        return ctx

    def get_queryset(self):
        category_slug = self.kwargs['category']
        cat = get_object_or_404(Category, slug=category_slug)

        query_dict = self.request.GET
        args = query_dict.dict()

        qs = cat.products.all()

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

        if args:
            for k, v in args.items():
                k = k.lower()
                v = v.lower()
                for product in qs:
                    if product.specifications.get(k) is None or product.specifications[k].find(v) == -1:
                        qs = qs.exclude(id=product.id)
                        break

        if order_by:
            qs = qs.order_by(order_by)

        return qs

    def get(self, request, *args, **kwargs):
        if request.GET.get('paginate_by'):
            self.paginate_by = request.GET['paginate_by']
        return super().get(request, *args, **kwargs)


class AnnouncementDetailView(DetailView):
    model = Announcement


class ProductDetailView(ListView):
    template_name = 'core/product_detail.html'
    model = Review
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        ctx = self.get_context_data(**kwargs)
        return render(request, 'core/product_detail.html', ctx)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_object()
        ctx['object'] = obj
        ctx['max_cnt'] = MAX_PRODUCT_IN_BASKET_OR_ORDER_COUNT

        if self.request.user.is_authenticated:
            review = Review.objects.get_review_or_unsaved_blank_review(
                product=obj,
                user=self.request.user
            )
            if review.id:
                review_form_url = reverse('core:update-review', kwargs={'slug': obj.slug, 'pk': review.id})
            else:
                review_form_url = reverse('core:create-review', kwargs={'slug': obj.slug})
            review_form = ReviewForm(instance=review)
            ctx['review_form'] = review_form
            ctx['review_form_url'] = review_form_url

        return ctx

    def get_queryset(self):
        product = self.get_object()
        return Review.objects.filter(product=product)

    def get_object(self):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug__iexact=slug)
        return product


class CreateReviewView(LoginRequiredMixin, CreateView):
    login_url = '/user/login'
    form_class = ReviewForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['product'] = Product.objects.get(slug=self.kwargs['slug']).id
        return initial

    def get_success_url(self):
        product_slug = self.object.product.slug
        self.object.product.update_rating()
        return reverse('core:product', kwargs={'slug': product_slug})

    def render_to_response(self, context, **response_kwargs):
        return redirect(to=self.get_success_url())


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login'
    form_class = ReviewForm
    queryset = Review.objects.all()

    def get_object(self, queryset=None):
        review = super().get_object(queryset)
        user = self.request.user
        if review.user != user:
            raise PermissionDenied('Cannot change another user review')
        return review

    def get_success_url(self):
        product_slug = self.object.product.slug
        self.object.product.update_rating()
        return reverse('core:product', kwargs={'slug': product_slug})

    def render_to_response(self, context, **response_kwargs):
        product_slug = context['object'].slug
        product_detail_url = reverse('core:product', kwargs={'slug': product_slug})
        return redirect(to=product_detail_url)


class AddToBasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def post(self, request, *args, **kwargs):
        count = request.POST['count']
        user = request.user
        basket = user.basket

        try:
            count = int(count)
            if count > 0:
                product_id = int(request.POST['id'])
                product = get_object_or_404(Product, id=product_id)

                basket.total_count += 1
                basket.save()

                ProductInBasket.objects.create(product=product, basket=user.basket, count=count)
        except ValueError:
            logger.warning(f'add to basket, request.POST = {request.POST}')
            return HttpResponseNotFound()

        return JsonResponse({'count': basket.total_count})


class UpdateBasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def post(self, request, *args, **kwargs):
        basket = request.user.basket
        pairs = request.POST['pairs']
        code = request.POST['code']

        pairs = ast.literal_eval(pairs)
        try:
            for key, value in pairs.items():
                val = int(value)
                if val > 0 and val <= MAX_PRODUCT_IN_BASKET_OR_ORDER_COUNT:
                    product_in_basket = get_object_or_404(ProductInBasket, id=key)
                    product_in_basket.count = val
                    product_in_basket.save()

            if re.fullmatch(UUID4_PATTERN, code):
                if Coupone.objects.get(code=code):
                    basket.coupone_code = code
                    basket.save()
        except ValueError:
            logger.warning(f'update basket, pairs = {pairs}, code = {code}')
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})


class RemoveFromBasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def post(self, request, *args, **kwargs):
        product_id = request.POST['id']
        basket = request.user.basket

        product_in_basket = ProductInBasket.objects.get(id__iexact=product_id)

        if product_in_basket:
            basket.total_count -= 1
            basket.save()

            product_in_basket.delete()
            total = basket.get_total_price()
        else:
            logger.warning(f'remove from basket, id = {id}')

        return JsonResponse({'total': total, 'count': basket.total_count})


class BasketView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def get(self, request, *args, **kwargs):
        basket = request.user.basket
        products = ProductInBasket.objects.filter(basket__id=basket.id)

        return render(
            request,
            'core/basket.html',
            {
                'products': products,
                'total': basket.get_total_price(),
                'max_cnt': MAX_PRODUCT_IN_BASKET_OR_ORDER_COUNT,
                'code': basket.coupone_code,
            }
        )


class ConfirmOrderView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def get(self, request, *args, **kwargs):
        basket = request.user.basket
        products_in_basket = ProductInBasket.objects.filter(basket__id=basket.id)
        total = basket.get_total_price()

        ctx = {
            'products_in_basket': products_in_basket,
            'total': total,
        }

        code = basket.coupone_code
        if code:
            discount = Coupone.objects.get(code=code).discount
            ctx['discount'] = discount
            total = round(float(total) * (1 - discount / 100), 2)
            ctx['total_with_discount'] = total

        return render(request, 'core/confirm_order.html', ctx)


class MakeOrderView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def post(self, request, *args, **kwargs):
        user = request.user
        basket = user.basket

        products_in_basket = ProductInBasket.objects.filter(basket__id=basket.id)
        total = basket.get_total_price()
        code = basket.coupone_code
        discount = 0

        if code:
            coupone = Coupone.objects.get(code=code)
            discount = coupone.discount
            total = round(float(total) * (1 - discount / 100), 2)
            basket.coupone_code = None
            coupone.delete()

        order = Order.objects.create(user=user, total_price=total, discount=discount)

        for product_in_basket in products_in_basket.all():
            ProductInOrder.objects.create(
                product=product_in_basket.product,
                order=order,
                count=product_in_basket.count
            )
            product_in_basket.delete()

        basket.total_count = 0
        basket.save()

        return redirect('core:index')


class OrderListView(PermissionRequiredMixin, ListView):
    model = Order
    paginate_by = 10
    template_name = 'core/orders.html'
    login_url = '/user/login'

    permission_required = ('order.can_change')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        forms = []
        products = []
        orders = ctx['object_list']
        for order in orders:
            forms.append(OrderForm(instance=order))
            products.append(ProductInOrder.objects.filter(order__id=order.id))
        orders_forms_products = zip(orders, forms, products)
        ctx['object_list'] = orders_forms_products
        return ctx


class UpdateOrderView(PermissionRequiredMixin, UpdateView):
    login_url = '/user/login'
    permission_required = ('order.can_change')
    form_class = OrderForm
    queryset = Order.objects.all()

    def get_success_url(self):
        return reverse('core:orders')
