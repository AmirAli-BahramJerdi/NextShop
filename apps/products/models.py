from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="اسلاگ")
    icon = models.CharField(max_length=50, verbose_name="آیکون")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name="تصویر")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name="دسته‌بندی والد")
    is_featured = models.BooleanField(default=False, verbose_name="نمایش در صفحه اصلی")
    product_count = models.PositiveIntegerField(default=0, verbose_name="تعداد محصولات")
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    BADGE_CHOICES = (
        ('none', 'بدون نشان'),
        ('sale', 'تخفیف'),
        ('new', 'جدید'),
        ('hot', 'پیشنهاد ویژه'),
        ('bestseller', 'پرفروش'),
        ('limited', 'محدود'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="اسلاگ")
    description = RichTextField(verbose_name="توضیحات")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    discount_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="قیمت با تخفیف")
    image = models.ImageField(upload_to='products/', verbose_name="تصویر اصلی")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    sold = models.PositiveIntegerField(default=0, verbose_name="فروش رفته")
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='none', verbose_name="نشان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_featured = models.BooleanField(default=False, verbose_name="محصول ویژه")
    is_special_offer = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name="امتیاز")
    rating_count = models.PositiveIntegerField(default=0, verbose_name="تعداد امتیازدهی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    
    def get_discount_percentage(self):
        if self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        # Update category product count
        self.category.product_count = self.category.products.count()
        self.category.save()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="محصول")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="تصویر")
    
    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"
    
    def __str__(self):
        return f"تصویر {self.id} برای {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="محصول")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="کاربر")
    rating = models.PositiveSmallIntegerField(verbose_name="امتیاز")
    comment = models.TextField(verbose_name="نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f"نظر {self.user.username} برای {self.product.name}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update product rating
        product = self.product
        reviews = product.reviews.all()
        if reviews:
            product.rating = sum(review.rating for review in reviews) / reviews.count()
            if is_new:
                product.rating_count += 1
            product.save()


class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن")
    
    class Meta:
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.product.name} در علاقه‌مندی‌های {self.user.username}"