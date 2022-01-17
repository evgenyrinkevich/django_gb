
from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='index'),
    path('order/create/', ordersapp.OrderCreate.as_view(), name='order_create'),
    path('order/update/<int:pk>/', ordersapp.OrderUpdate.as_view(), name='order_update'),
    path('order/detail/<int:pk>/', ordersapp.OrderDetail.as_view(), name='order_detail'),
    path('order/delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),

    path('order/update/price/<int:pk>/', ordersapp.order_item_price_update, name='order_price_update'),
]
