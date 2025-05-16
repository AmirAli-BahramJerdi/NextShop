from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'total_items', 'total_price', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'session_id')
    inlines = [CartItemInline]
    readonly_fields = ('total_price', 'total_items')
    
    def total_price(self, obj):
        return f"{obj.total_price:,} تومان"
    total_price.short_description = "مجموع قیمت"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    list_filter = ('cart',)
    search_fields = ('cart__user__username', 'product__name')
    
    def total_price(self, obj):
        return f"{obj.total_price:,} تومان"
    total_price.short_description = "قیمت کل"