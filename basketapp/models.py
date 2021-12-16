from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)

    @property
    def product_cost(self):
        """cost of all products of this category"""
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        """total quantity in user's basket"""
        _items = self.user.basket.all()
        _total_quantity = sum(map(lambda x: x.quantity, _items))
        return _total_quantity

    @property
    def total_cost(self):
        """total cost for user"""
        _items = self.user.basket.all()
        _total_quantity = sum(map(lambda x: x.product_cost, _items))
        return _total_quantity


