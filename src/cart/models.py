from django.db import models
from django.conf import settings
from core.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    price_total = models.FloatField(null=True)
    price_subtotal = models.FloatField(null=True)

    class Meta:
        unique_together = ('user', 'session_key')

    def update_subtotal(self):
        subtotal = self.items.all().aggregate(sum=models.Sum('total_price'))
        self.price_subtotal = subtotal['sum']
        self.save()

    def get_total_quantity_of_items(self):
        quantity = self.items.all().aggregate(sum=models.Sum('quantity'))
        return quantity['sum']

    def get_total(self):
        total = 0
        for item_in_cart in self.items.all():
            total += item_in_cart.get_total_item_price()
        return total

    def __str__(self):
        return f"Cart id: {self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, related_name='items', blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField(null=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.product.title

    def get_total_item_price(self):
        self.total_price = self.quantity * self.product.price
        return self.total_price
