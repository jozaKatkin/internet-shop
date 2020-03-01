from uuid import uuid4

from django.conf import settings
from django.db import models

TITLE = (
    ('processing', 'Processing'),
    ('waiting', 'Waiting to pick up for delivery'),
    ('delivery', 'In delivery'),
    ('done', 'Delivered'),
    ('x', 'Cancelled'),
)


class Category(models.Model):
    title = models.CharField(max_length=64, blank=False, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Category {self.title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def all(self):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length=64)
    price = models.FloatField()

    # discount = models.IntegerField(default=0)
    # short_description = models.TextField(blank=True, default=None)

    description = models.TextField(blank=True, default=None)
    image = models.ImageField(upload_to='static/media/products_images/')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    category = models.ManyToManyField('Category', blank=True)

    objects = ProductManager()

    def __str__(self):
        return f"Product {self.title}, {self.price}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ItemInOrder(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('Product', null=True, on_delete=models.DO_NOTHING, related_name='items_in_order')
    total_price = models.FloatField(null=True)

    def __str__(self):
        return f"Order item {self.product.title} x {self.quantity} pcs"

    class Meta:
        verbose_name = 'Item in order'
        verbose_name_plural = 'Items in order'

    def get_total_item_price(self):
        self.total_price = self.quantity * self.product.price
        return self.total_price


class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.CASCADE)
    cart = models.ForeignKey('cart.Cart', on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=128)
    comment = models.TextField(blank=True)
    delivery_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=TITLE, default='Processing', max_length=150)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created_at = timezone.now()
    #     self.ordered_at = timezone.now()
    #     return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def get_total(self):
        total = 0
        for item_in_order in self.items.all():
            total += item_in_order.get_total_item_price()
        return total

    def get_short_uuid(self):
        uuid = str(self.uuid).split('-')
        return f"{uuid[0]}-{uuid[1]}"

    def get_cart_items(self):
        return self.cart.items.all()

    def create_order_items(self):
        cart_items = self.cart.items.all()
        for item in cart_items:
            ItemInOrder.objects.create(order=self, product=item.product,
                                       quantity=item.quantity)
