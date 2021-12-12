import os
import json

from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.conf import settings


def load_from_json(file_name):
    with open(os.path.join(settings.JSON_PATH, f'{file_name}.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('product_categories')

        ProductCategory.objects.all().delete()
        [ProductCategory.objects.create(**category) for category in categories]

        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            _category = ProductCategory.objects.filter(name=category_name).first()
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', email='django@gb.ru', password='geekbrains')

