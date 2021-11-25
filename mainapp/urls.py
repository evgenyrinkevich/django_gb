
from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('products/', mainapp.products, name='products'),
    path('contact/', mainapp.contact, name='contact'),
    path('about/', mainapp.about, name='about'),
    path('categories/<int:pk>/', mainapp.products_by_category, name='category'),
]
