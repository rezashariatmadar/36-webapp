"""Shared cafe cart/session helpers used by API handlers."""

CART_SCHEMA_VERSION = 1
MAX_CART_ITEMS = 50
MAX_PER_ITEM = 20


def get_cart(request):
    """
    Retrieve a schema-versioned cart from session.
    Resets malformed carts to an empty dict.
    """
    cart = request.session.get("cart", {})
    version = request.session.get("cart_v")
    if not isinstance(cart, dict):
        cart = {}
    if version != CART_SCHEMA_VERSION:
        request.session["cart_v"] = CART_SCHEMA_VERSION
        request.session["cart"] = cart
    return cart


def save_cart(request, cart):
    request.session["cart"] = cart
    request.session["cart_v"] = CART_SCHEMA_VERSION
