
from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('product/<int:pk>/', mainapp.product_page, name='product_page'),
    path('contact/', mainapp.contact, name='contact'),
    path('about/', mainapp.about, name='about'),
    path('categories/<int:pk>/', mainapp.products_by_category, name='category'),
]
