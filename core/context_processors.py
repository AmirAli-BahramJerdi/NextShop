from .utils import get_or_create_cart


def cart_processor(request):
    """
    Context processor to make cart available in all templates
    """
    try:
        cart = get_or_create_cart(request)
        return {'cart': cart}
    except:
        return {'cart': None}