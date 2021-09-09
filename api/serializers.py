from rest_framework import serializers

from products.models import ProductModel, CategoryModel, ProductTagModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'title', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTagModel
        fields = ['id', 'title', 'created_at']


class ProductModelSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = ProductModel
        exclude = ['short_description_uz', 'short_description_en', 'short_description_ru',
                   'title_uz', 'title_en', 'title_ru',
                   'long_description_en', 'long_description_ru', 'long_description_uz'
                   ]
