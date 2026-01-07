def cart_context(request):
    """
    Context processor to provide the cart count globally.
    """
    cart = request.session.get('cart', {})
    # Simple count of total items in cart
    cart_items_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return {
        'cart_count': cart_items_count
    }
