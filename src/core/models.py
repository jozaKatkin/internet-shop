from django.conf import settings
from django.db import models
from django.utils import timezone

TITLE = (
    (1, 'Processing'),
    (2, 'Waiting to pick up for delivery'),
    (3, 'In delivery'),
    (4, 'Delivered'),
    (5, 'Cancelled'),
)


class Category(models.Model):
    title = models.CharField(max_length=64, blank=False, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Category {self.title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=64)
    price = models.FloatField()
    # discount = models.IntegerField(default=0)

    # short_description = models.TextField(blank=True, default=None)
    description = models.TextField(blank=True, default=None)
    image = models.ImageField(upload_to='products_images/')
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, related_name='products')

    def __str__(self):
        return f"Product {self.title}, {self.price}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ItemInOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey('Product', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order item {self.product.title} x {self.quantity} pcs"

    class Meta:
        verbose_name = 'Item in order'
        verbose_name_plural = 'Items in order'

    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=128)
    comment = models.TextField(blank=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField('ItemInOrder')
    delivery_time = models.TimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField()
    status = models.IntegerField(choices=TITLE, default=1)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.ordered_at = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


