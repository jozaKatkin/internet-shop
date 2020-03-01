from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields]

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CartItem._meta.fields]

    class Meta:
        model = CartItem


admin.site.register(CartItem, CartItemAdmin)
