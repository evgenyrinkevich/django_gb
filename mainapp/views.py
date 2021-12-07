from random import choice

from django.shortcuts import render, get_object_or_404
import json
from .models import ProductCategory, Product


def get_basket(request):
    return request.user.is_authenticated and request.user.basket.all() or []


def index(request):
    hot_offer_pk = choice(Product.objects.values_list('pk', flat=True))
    hot_offer = Product.objects.get(pk=hot_offer_pk)

    same_products = hot_offer.category.product_set.exclude(pk=hot_offer_pk)
    context = {'page_title': 'home',
               'same_products': same_products,
               'basket': get_basket(request),
               'hot_offer': hot_offer
               }
    print(hot_offer)
    return render(request, 'mainapp/index.html', context)


def about(request):
    with open("mainapp/fixtures/about.json", encoding="utf-8") as json_file:
        json_object = json.load(json_file)
        json_file.close()

    context = {
        'page_title': 'about',
        'json_object': json_object,
        'basket': get_basket(request)
    }

    return render(request, 'mainapp/about.html', context)


def products(request):
    products_list = Product.objects.all()
    product_category = ProductCategory.objects.all()
    context = {'page_title': 'products',
               'products': products_list,
               'categories': product_category,
               'basket': get_basket(request)
               }

    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open("mainapp/fixtures/contact.json", encoding="utf-8") as json_file:
        json_object = json.load(json_file)
        json_file.close()
    context = {
        'page_title': 'contact',
        'json_object': json_object,
        'basket': get_basket(request)
    }

    return render(request, 'mainapp/contact.html', context)


def products_by_category(request, pk=None):
    product_categories = ProductCategory.objects.all()
    category = get_object_or_404(ProductCategory, pk=pk)
    prods_by_category = category.product_set.all()
    context = {'page_title': category.name,
               'products': prods_by_category,
               'categories': product_categories,
               'basket': get_basket(request)
               }
    return render(request, 'mainapp/products.html', context)

