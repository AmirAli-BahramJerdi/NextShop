from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Template URLS:
        path('admin/', admin.site.urls),
        path('accounts/', include('allauth.urls')),
        path('products/', include('apps.products.urls')),
        path('cart/', include('apps.cart.urls')),
        path('orders/', include('apps.orders.urls')),
        path('', include('apps.main.urls')),
    # API URLS:
        # path('api/', include('api.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# # handlers
handler400 = 'core.handlers.error_400'
handler403 = 'core.handlers.error_403'
handler404 = 'core.handlers.error_404'
handler500 = 'core.handlers.error_500'