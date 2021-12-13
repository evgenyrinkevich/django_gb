
from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('user/create/', adminapp.user_create, name='user_create'),
    path('user/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('user/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('user/restore/<int:pk>/', adminapp.user_restore, name='user_restore'),

    path('category/create/', adminapp.category_create, name='category_create'),
    path('category/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/list/', adminapp.categories_list, name='categories_list'),
    path('category/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('category/restore/<int:pk>/', adminapp.category_restore, name='category_restore'),
    path('category/<int:pk>/products/', adminapp.category_products, name='category_products'),

]
