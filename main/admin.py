from django.contrib import admin
from .models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'image_tag', 'is_featured', 'price')
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product', 'product_qty')
admin.site.register(Cart, CartAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product')
admin.site.register(Wishlist, WishlistAdmin)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Banner)
