from django.shortcuts import render
import json
from .models import ProductCategory, Product


def index(request):

    products_list = Product.objects.all()
    context = {'page_title': 'home',
               'products': products_list}

    return render(request, 'mainapp/index.html', context)


def about(request):

    with open("mainapp/fixtures/about.json", encoding="utf-8") as json_file:
        json_object = json.load(json_file)
        json_file.close()

    context = json_object

    return render(request, 'mainapp/about.html', context)


def products(request):

    products_list = Product.objects.all()
    product_category = ProductCategory.objects.all()
    context = {'page_title': 'products',
               'products': products_list,
               'categories': product_category}

    return render(request, 'mainapp/products.html', context)


def contact(request):

    with open("mainapp/fixtures/contact.json", encoding="utf-8") as json_file:
        json_object = json.load(json_file)
        json_file.close()
    context = json_object

    return render(request, 'mainapp/contact.html', context)


def products_by_category(request, pk=None):
    prods_by_category = Product.objects.filter(category=pk)
    product_category = ProductCategory.objects.all()
    context = {'page_title': prods_by_category[0].category.name if prods_by_category else 'Error',
               'products': prods_by_category,
               'categories': product_category
               }
    return render(request, 'mainapp/products.html', context)

