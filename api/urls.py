from django.urls import path
from . import views



app_name = 'api'



urlpatterns = [
    path('user_create/', views.UserCreateApiView.as_view(), name='user_create'),
    path('login/', views.LoginUserApiView.as_view(), name='login'),
    path('edit_user/', views.EditUserApiView.as_view(), name='edit_user'),
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    path('address_create/', views.AddressApiView.as_view(), name='address_create'),
    path('address_detail/', views.AddressApiView.as_view(), name='address_detail'),
    path('address_update/', views.AddressApiView.as_view(), name='address_update'),
    path('address_delete/', views.AddressApiView.as_view(), name='address_delete'),
    path('address_list/', views.AddressListApiView.as_view(), name='address_list'),
    path('user_list/', views.UserListApiView.as_view(), name='user_list'),
    path('user_detail/', views.UserDetailApiView.as_view(), name='user_detail'),
    path('news_letter/', views.NewsletterApiView.as_view(), name='news_letter'),
    path('review/', views.ReviewApiView.as_view(), name='review'),
    path('wish_product/', views.WishlistApiView.as_view(), name='wish_product'),
    path('wishlist/', views.WishlistApiView.as_view(), name='wishlist'),
    path('wish_delete/', views.WishlistApiView.as_view(), name='wish_delete'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove_as_cart/', views.RemoveFromCartView.as_view(), name='remove_as_cart'),
    path('cart_detail/', views.CartDetail.as_view(), name='cart_detail'),
    path('order_create/', views.OrderApiView.as_view(), name='order_create'),
    path('order_list/', views.OrderListApiView.as_view(), name='order_list'),
    path('payment_create/', views.PaymentApiView.as_view(), name='payment_create'),
    path('payment_list/', views.PaymentApiView.as_view(), name='payment_list'),
]