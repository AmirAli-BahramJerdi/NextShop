from django.contrib import admin
from .models import Profile, Address


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city')
    search_fields = ('user__username', 'user__email', 'phone', 'city')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'recipient_name', 'city', 'address_type', 'is_default')
    list_filter = ('address_type', 'is_default', 'city')
    search_fields = ('user__username', 'recipient_name', 'address', 'city')