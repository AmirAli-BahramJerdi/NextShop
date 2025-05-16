from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
        ('refunded', 'مسترد شده'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    city = models.CharField(max_length=100, verbose_name="شهر")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    total_price = models.PositiveIntegerField(verbose_name="مبلغ کل")
    shipping_cost = models.PositiveIntegerField(default=0, verbose_name="هزینه ارسال")
    tracking_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="کد پیگیری")
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شناسه پرداخت")
    notes = models.TextField(blank=True, null=True, verbose_name="یادداشت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"سفارش #{self.id} - {self.user.username}"
    
    @property
    def grand_total(self):
        return self.total_price + self.shipping_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    price = models.PositiveIntegerField(verbose_name="قیمت واحد")
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    
    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"
    
    def __str__(self):
        return f"{self.quantity} عدد {self.product.name} در سفارش #{self.order.id}"
    
    @property
    def total_price(self):
        return self.price * self.quantity


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
        ('refunded', 'مسترد شده'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name="سفارش")
    amount = models.PositiveIntegerField(verbose_name="مبلغ")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شناسه تراکنش")
    payment_method = models.CharField(max_length=50, verbose_name="روش پرداخت")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"پرداخت {self.amount:,} تومان برای سفارش #{self.order.id}"