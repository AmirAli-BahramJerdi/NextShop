from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'total_price')
    
    def total_price(self, obj):
        return f"{obj.total_price:,} تومان"
    total_price.short_description = "قیمت کل"


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('amount', 'transaction_id', 'payment_method', 'status', 'created_at')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'full_name', 'email', 'phone', 'tracking_code')
    readonly_fields = ('user', 'total_price', 'created_at')
    inlines = [OrderItemInline, PaymentInline]
    fieldsets = (
        ('اطلاعات مشتری', {
            'fields': ('user', 'full_name', 'email', 'phone')
        }),
        ('اطلاعات ارسال', {
            'fields': ('address', 'postal_code', 'city')
        }),
        ('اطلاعات سفارش', {
            'fields': ('status', 'total_price', 'shipping_cost', 'tracking_code', 'payment_id', 'notes')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def total_price(self, obj):
        return f"{obj.total_price:,} تومان"
    total_price.short_description = "مبلغ کل"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order__id', 'transaction_id')
    readonly_fields = ('order', 'amount', 'created_at')