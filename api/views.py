from rest_framework.generics import ListAPIView

from api.serializers import ProductModelSerializer
from products.models import ProductModel


class ProductListAPIView(ListAPIView):
    serializer_class = ProductModelSerializer

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