from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="کاربر")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تماس")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد پستی")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="شهر")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="تصویر پروفایل")
    
    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"
    
    def __str__(self):
        return f"پروفایل {self.user.username}"


class Address(models.Model):
    ADDRESS_TYPES = (
        ('home', 'منزل'),
        ('work', 'محل کار'),
        ('other', 'سایر'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="کاربر")
    title = models.CharField(max_length=100, verbose_name="عنوان آدرس")
    recipient_name = models.CharField(max_length=100, verbose_name="نام گیرنده")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    city = models.CharField(max_length=100, verbose_name="شهر")
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home', verbose_name="نوع آدرس")
    is_default = models.BooleanField(default=False, verbose_name="آدرس پیش‌فرض")
    
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
        ordering = ['-is_default', 'id']
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
        ordering = ['-is_default', 'id']
    
    def __str__(self):
        return f"{self.title} - {self.recipient_name}"
    
    def save(self, *args, **kwargs):
        # If this address is set as default, unset any other default addresses
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)