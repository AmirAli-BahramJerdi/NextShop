from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem
from core.utils import get_or_create_cart


class CartView(TemplateView):
    template_name = 'cart/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        context['cart'] = cart
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check if product is in stock
        if product.stock < quantity:
            messages.error(request, 'متاسفانه موجودی کافی نیست.')
            return redirect('product_detail', slug=product.slug)
        
        # Get or create cart
        cart = get_or_create_cart(request)
        
        # Check if product already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if product already in cart
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, 'محصول به سبد خرید اضافه شد.')
        
        # If AJAX request, return JSON response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'محصول به سبد خرید اضافه شد.',
                'cart_total': cart.total_items
            })
        
        return redirect('cart')


class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        action = request.POST.get('action')
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Check if cart belongs to current user/session
        cart = get_or_create_cart(request)
        if cart_item.cart.id != cart.id:
            messages.error(request, 'خطا در بروزرسانی سبد خرید.')
            return redirect('cart')
        
        if action == 'increase':
            # Check stock
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, 'موجودی کافی نیست.')
        
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        
        elif action == 'remove':
            cart_item.delete()
            messages.success(request, 'محصول از سبد خرید حذف شد.')
        
        # If AJAX request, return JSON response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': cart.total_items,
                'item_total': cart_item.total_price if action != 'remove' else 0,
                'cart_subtotal': cart.total_price
            })
        
        return redirect('cart')