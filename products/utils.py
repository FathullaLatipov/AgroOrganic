from django.db.models import Sum

from products.models import ProductModel


def get_cart_data(cart):
    return len(cart)


def get_wishlist_data(wishlist):
    return len(wishlist)
