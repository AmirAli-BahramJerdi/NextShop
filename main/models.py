from django.db import models
from ckeditor.fields import RichTextField


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    subtitle = models.CharField(max_length=300, verbose_name="زیرعنوان")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='banners/', verbose_name="تصویر")
    button_text = models.CharField(max_length=50, verbose_name="متن دکمه")
    button_link = models.CharField(max_length=200, verbose_name="لینک دکمه")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنرها"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Feature(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    description = models.CharField(max_length=200, verbose_name="توضیحات")
    icon = models.CharField(max_length=50, verbose_name="آیکون")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="ترتیب")
    
    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی‌ها"
        ordering = ['order']
    
    def __str__(self):
        return self.title


class PromoBanner(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    subtitle = models.CharField(max_length=300, verbose_name="زیرعنوان")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='promos/', verbose_name="تصویر")
    button_text = models.CharField(max_length=50, verbose_name="متن دکمه")
    button_link = models.CharField(max_length=200, verbose_name="لینک دکمه")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = "بنر تبلیغاتی"
        verbose_name_plural = "بنرهای تبلیغاتی"
    
    def __str__(self):
        return self.title


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    
    class Meta:
        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه"
    
    def __str__(self):
        return self.email