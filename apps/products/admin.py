from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Wishlist


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'product_count', 'is_featured')
    list_filter = ('is_featured', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'sold', 'badge', 'is_active')
    list_filter = ('is_active', 'is_featured', 'is_special_offer', 'badge', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ReviewInline]
    list_editable = ('price', 'discount_price', 'stock', 'badge', 'is_active')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'discount_price', 'stock', 'sold')
        }),
        ('تنظیمات نمایش', {
            'fields': ('badge', 'is_active', 'is_featured', 'is_special_offer')
        }),
        ('امتیازدهی', {
            'fields': ('rating', 'rating_count'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('rating', 'rating_count', 'sold')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('product', 'user', 'rating', 'comment', 'created_at')
    
    def has_add_permission(self, request):
        return False


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')