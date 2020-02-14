from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=64, blank=False, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Category {self.title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=64, blank=True, default=None)
    price = models.FloatField()
    # discount = models.IntegerField(default=0)

    # short_description = models.TextField(blank=True, default=None)
    description = models.TextField(blank=True, default=None)
    image = models.ImageField(upload_to='products_images/')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, related_name='products')

    def __str__(self):
        return f"Product {self.title}, {self.price}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Status(models.Model):
    TITLE = (
        (1, 'Processing'),
        (2, 'Waiting to pick up for delivery'),
        (3, 'In delivery'),
        (4, 'Delivered'),
        (5, 'Cancelled'),
    )
    title = models.IntegerField(choices=TITLE, blank=True, null=True, default=1)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"Status {self.title}, updated {self.updated}"

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class ItemInOrder(models.Model):
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    product = models.OneToOneField('Product', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order item {self.product.title} x {self.quantity} pcs"

    class Meta:
        verbose_name = 'Item in order'
        verbose_name_plural = 'Items in order'

    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    customer = models.CharField(max_length=128, null=True, blank=True, default=None, help_text='First Name')
    status = models.ForeignKey('Status', null=True, on_delete=models.CASCADE, related_name='orders')
    email = models.EmailField(default=None, help_text='Email', blank=True, null=True)
    phone = models.CharField(max_length=48, blank=False, default=None)
    address = models.CharField(max_length=128, blank=False, null=False, default=None)
    comment = models.TextField(default=None, blank=True)
    is_ordered = models.BooleanField(default=True)
    items = models.ManyToManyField('ItemInOrder', related_name='items')

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"Order {self.id} {self.status.title}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


