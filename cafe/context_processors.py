def cart_context(request):
    """
    Context processor to provide the cart count globally.
    """
    if not hasattr(request, 'session'):
        return {'cart_count': 0}
        
    cart = request.session.get('cart', {})
    # Simple count of total items in cart
    try:
        cart_items_count = sum(cart.values()) if isinstance(cart, dict) else 0
    except (AttributeError, TypeError):
        cart_items_count = 0
        
    return {
        'cart_count': cart_items_count
    }