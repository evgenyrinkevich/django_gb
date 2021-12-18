from random import choice

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import json
from .models import ProductCategory, Product


def get_basket(request):
    return request.user.is_authenticated and request.user.basket.all() or []


def get_menu():
    return ProductCategory.objects.filter(is_active=True)


def index(request):
    hot_offer_pk = choice(Product.objects.filter(is_active=True).values_list('pk', flat=True))
    hot_offer = Product.objects.get(pk=hot_offer_pk)

    same_products = hot_offer.category.product_set.filter(is_active=True).exclude(pk=hot_offer_pk)[:3]
    context = {'page_title': 'home',
               'same_products': same_products,
               'basket': get_basket(request),
               'hot_offer': hot_offer
               }
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


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'page_title': product.name,
               'category': product.category,
               'categories': get_menu(),
               'basket': get_basket(request),
               'product': product
               }
    return render(request, 'mainapp/product.html', context)


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
    if pk == 0:
        category = {'pk': 0, 'name': 'all'}
        prods_by_category = Product.objects.filter(is_active=True).order_by('?')
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        prods_by_category = category.product_set.filter(is_active=True)
    products_paginator = Paginator(prods_by_category, 3)
    page = request.GET.get('page')
    try:
        prods_by_category = products_paginator.get_page(page)
    except PageNotAnInteger:
        prods_by_category = products_paginator.page(1)
    except EmptyPage:
        prods_by_category = products_paginator.page(products_paginator.num_pages)
    context = {'page_title': 'catalog',
               'products': prods_by_category,
               'categories': get_menu(),
               'basket': get_basket(request),
               'category': category
               }
    return render(request, 'mainapp/products.html', context)

