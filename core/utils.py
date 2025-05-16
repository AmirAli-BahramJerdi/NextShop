from apps.cart.models import Cart


def get_or_create_cart(request):
    """
    Get existing cart or create a new one based on user authentication status
    """
    if request.user.is_authenticated:
        # Get or create cart for authenticated user
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            defaults={'session_id': None}
        )
        
        # If user has a session cart, merge it with user cart
        session_id = request.session.session_key
        if session_id:
            session_cart = Cart.objects.filter(session_id=session_id).first()
            if session_cart:
                # Merge items from session cart to user cart
                for item in session_cart.items.all():
                    # Check if product already in user cart
                    user_item = cart.items.filter(product=item.product).first()
                    if user_item:
                        user_item.quantity += item.quantity
                        user_item.save()
                    else:
                        item.cart = cart
                        item.save()
                
                # Delete session cart
                session_cart.delete()
    else:
        # Get or create cart for anonymous user
        if not request.session.session_key:
            request.session.create()
        
        session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            session_id=session_id,
            defaults={'user': None}
        )
    
    return cart