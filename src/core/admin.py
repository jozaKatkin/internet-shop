
from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status


admin.site.register(Status, StatusAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class ItemInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ItemInOrder._meta.fields]

    class Meta:
        model = ItemInOrder


admin.site.register(ItemInOrder, ItemInOrderAdmin)


