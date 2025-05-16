from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<int:order_id>/', views.PaymentView.as_view(), name='payment'),
    path('my-orders/', views.OrderListView.as_view(), name='order_list'),
    path('my-orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]