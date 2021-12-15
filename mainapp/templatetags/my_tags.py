from django import template
from django.conf import settings

register = template.Library()


def media_folder_products(string):
    """
    Adds relative URL-path to products media files
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    """
    Adds relative URL-path to users media files
    users_avatar/user1.jpg --> /media/users_avatar/user1.jpg
    """
    if not string:
        string = 'users_avatar/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_products', media_folder_products)
