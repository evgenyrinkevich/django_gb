from django.shortcuts import render
import json


# Create your views here.
def index(request):

    with open("mainapp/database/products.json") as json_file:
        json_object = json.load(json_file)
        json_file.close()

    context = {'page_title': 'home',
               'products': [product for product in json_object]}

    return render(request, 'mainapp/index.html', context)


def about(request):

    with open("mainapp/database/about.json") as json_file:
        json_object = json.load(json_file)
        json_file.close()

    context = json_object

    return render(request, 'mainapp/about.html', context)


def products(request):

    with open("mainapp/database/products.json") as json_file:
        json_object = json.load(json_file)
        json_file.close()

    context = {'page_title': 'products',
               'products': [product for product in json_object]}

    return render(request, 'mainapp/products.html', context)


def contact(request):

    with open("mainapp/database/contact.json") as json_file:
        json_object = json.load(json_file)
        json_file.close()
    context = json_object

    return render(request, 'mainapp/contact.html', context)
