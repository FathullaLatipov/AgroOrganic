from django.contrib import messages
from django.db.models import Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.response import Response

from products.forms import CommentModelForm
from products.models import ProductModel, ProductTagModel, CategoryModel
from products.utils import get_cart_data


class ProductsListView(ListView):
    template_name = 'shop.html'
    paginate_by = 6
    extra_context = {'title': 'Shop'}

    # search in q
    def get_queryset(self):
        qs = ProductModel.objects.order_by('-pk')

        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        sort = self.request.GET.get('sort')
        price = self.request.GET.get('price')

        if q:
            qs = qs.filter(title__icontains=q)

        if category:
            qs = qs.filter(category_id=category)

        if tag:
            qs = qs.filter(tags__id=tag)

        if price:
            price_from, price_to = price.split(';')
            qs = qs.filter(real_price__gte=price_from, real_price__lte=price_to)

        if sort:
            if sort == 'price':
                qs = qs.order_by('real_price')
            elif sort == '-price':
                qs = qs.order_by('-real_price')

        return qs

    # tags in shop
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = CategoryModel.objects.order_by('-pk')
        context['tags'] = ProductTagModel.objects.order_by('-pk')

        context['min_price'], context['max_price'] = ProductModel.objects.aggregate(
            Min('real_price'),
            Max("real_price")
        ).values()

        return context


class ProductDetailView(DetailView):
    template_name = 'single-product.html'
    model = ProductModel
    extra_context = {'title': 'Product'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.object.category.products.exclude(pk=self.object.pk)[:4]
        return context


class CommentCreateView(CreateView):
    template_name = 'single-product.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(ProductModel, pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products:detail', kwargs={'pk': self.kwargs['pk']})

    def add_to_cart(request, pk):
        cart = request.session.get('cart')

        if not cart:
            cart = []

        if pk in cart:
            cart.remove(pk)
        else:
            cart.append(pk)

        request.session['cart'] = cart

        return redirect(request.GET.get('next', '/'))


def add_to_wishlist(request, pk):
    try:
        product = ProductModel.objects.get(pk=pk)
    except ProductModel.DoesNotExist:
        return Response(data={'status': False})
    # if not wishlist:
    #     wishlist = []
    wishlist = request.session.get('wishlist', [])
    if product.pk in wishlist:
        wishlist.remove(product.pk)
        data = {'status': True, 'added': False}
    else:
        wishlist.append(product.pk)
        data = {'status': True, 'added': True}
    request.session['wishlist'] = wishlist

    data['wishlist_len'] = get_cart_data(wishlist)
    return JsonResponse(data)


class WishlistListView(ListView):
    template_name = 'wishlist.html'
    paginate_by = 7

    def get_queryset(self):
        return ProductModel.get_from_wishlist(self.request)


class CartListView(ListView):
    template_name = 'shopping-cart.html'

    def get_queryset(self):
        return ProductModel.get_from_cart(self.request)


def create_wishlist(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)

    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)
    else:
        product.wishlist.add(request.user)

    product.save()

    return redirect(request.GET.get('next', '/'))


def add_to_cart(request, pk):
    try:
        product = ProductModel.objects.get(pk=pk)
    except ProductModel.DoesNotExist:
        return JsonResponse(data={'status': False})

    cart = request.session.get('cart', [])
    # if not cart:
    #     cart = []

    if product.pk in cart:
        cart.remove(product.pk)
        data = {'status': True, 'added': False}
    else:
        cart.append(product.pk)
        data = {'status': True, 'added': True}
    request.session['cart'] = cart

    data['cart_len'] = get_cart_data(cart)
    return JsonResponse(data)
