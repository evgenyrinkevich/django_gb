from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'F'
    SENT_TO_PROCEED = 'S'
    PROCEEDED = 'P'
    PAID = 'D'
    READY = 'R'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'forming'),
        (SENT_TO_PROCEED, 'sent_to_proceed'),
        (PAID, 'paid'),
        (PROCEEDED, 'proceeded'),
        (READY, 'ready'),
        (CANCEL, 'cancel'),
    )

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def is_forming(self):
        return self.status == self.FORMING

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.orderitems.all()))

    @property
    def product_type_quantity(self):
        return self.orderitems.count()

    @property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.orderitems.all()))

    # delete method redefined
    def delete(self, using=None, keep_parents=False):
        self.orderitems.delete()

        self.is_active = False
        self.save()


class OrderItemQuerySet(models.QuerySet):
    def delete(self):
        for item in self:
            item.delete()


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()
