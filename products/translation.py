from modeltranslation.translator import translator, register, TranslationOptions

from products.models import CategoryModel, ProductModel, WidthModel, HeightModel, WeightModel


@register(CategoryModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)



@register(WidthModel)
class WidthTranslationOptions(TranslationOptions):
    fields = ('width',)


@register(HeightModel)
class HeightTranslationOptions(TranslationOptions):
    fields = ('height',)


@register(WeightModel)
class WeightTranslationOptions(TranslationOptions):
    fields = ('weight',)


@register(ProductModel)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'long_description', 'product_long_description')
