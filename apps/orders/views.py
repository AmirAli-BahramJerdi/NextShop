from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from core.utils import get_or_create_cart
from .models import Order, OrderItem, Payment
from .forms import CheckoutForm


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Get cart
        cart = get_or_create_cart(request)
        
        # Check if cart is empty
        if cart.items.count() == 0:
            messages.warning(request, 'سبد خرید شما خالی است.')
            return redirect('cart')
        
        # Check if products are in stock
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                messages.error(
                    request, 
                    f'متاسفانه موجودی محصول {item.product.name} کافی نیست. '
                    f'موجودی فعلی: {item.product.stock} عدد'
                )
                return redirect('cart')
        
        # Pre-fill form with user data
        initial_data = {}
        if request.user.first_name and request.user.last_name:
            initial_data['full_name'] = f"{request.user.first_name} {request.user.last_name}"
        initial_data['email'] = request.user.email
        
        form = CheckoutForm(initial=initial_data)
        
        return render(request, 'orders/checkout.html', {
            'form': form,
            'cart': cart,
            'shipping_cost': 50000,  # Fixed shipping cost for now
        })
    
    def post(self, request, *args, **kwargs):
        # Get cart
        cart = get_or_create_cart(request)
        
        # Check if cart is empty
        if cart.items.count() == 0:
            messages.warning(request, 'سبد خرید شما خالی است.')
            return redirect('cart')
        
        form = CheckoutForm(request.POST)
        if form.is_valid():
            shipping_cost = 50000  # Fixed shipping cost for now
            
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    postal_code=form.cleaned_data['postal_code'],
                    city=form.cleaned_data['city'],
                    total_price=cart.total_price,
                    shipping_cost=shipping_cost,
                    notes=form.cleaned_data.get('notes', '')
                )
                
                # Create order items
                for item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.price,
                        quantity=item.quantity
                    )
                    
                    # Update product stock and sold count
                    product = item.product
                    product.stock -= item.quantity
                    product.sold += item.quantity
                    product.save()
                
                # Create payment record
                payment = Payment.objects.create(
                    order=order,
                    amount=order.grand_total,
                    payment_method='online'
                )
                
                # Clear cart
                cart.items.all().delete()
                
                # Redirect to payment page
                return redirect(reverse('payment', kwargs={'order_id': order.id}))
        
        return render(request, 'orders/checkout.html', {
            'form': form,
            'cart': cart,
            'shipping_cost': 50000,  # Fixed shipping cost for now
        })


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'], user=request.user)
        
        # Check if order is already paid
        if order.status != 'pending':
            messages.warning(request, 'این سفارش قبلا پرداخت شده است.')
            return redirect('order_detail', order_id=order.id)
        
        return render(request, 'orders/payment.html', {'order': order})
    
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'], user=request.user)
        
        # Simulate successful payment (in a real app, this would integrate with a payment gateway)
        payment = order.payments.first()
        payment.status = 'completed'
        payment.transaction_id = f"DEMO-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        payment.save()
        
        # Update order status
        order.status = 'paid'
        order.payment_id = payment.transaction_id
        order.save()
        
        messages.success(request, 'پرداخت با موفقیت انجام شد. از خرید شما متشکریم!')
        return redirect('order_detail', order_id=order.id)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)