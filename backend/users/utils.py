from products.models import Favorite, AnonymousFavorite, Cart, AnonymousCart, CartProduct

def merge_favorites(user, session_key):
    if not session_key:
        return False
    
    anonymous_favorites = AnonymousFavorite.objects.filter(session_key=session_key)

    if not anonymous_favorites.exists():
        return False
    
    merged_count = 0

    for anonymous_favorite in anonymous_favorites:
        if not Favorite.objects.filter(user=user, product=anonymous_favorite.product).exists():
            Favorite.objects.create(user=user, product=anonymous_favorite.product)
            merged_count += 1
    
    anonymous_favorites.delete()
    
    return merged_count > 0

def merge_carts(user, session_key):
    if not session_key:
        return False
    
    cart, created = Cart.objects.get_or_create(user=user)

    try:
        anonymous_cart = AnonymousCart.objects.get(session_key=session_key)
    except AnonymousCart.DoesNotExist:
        return False
    
    guest_products = CartProduct.objects.filter(anonymous_cart=anonymous_cart, cart=None)

    if not guest_products.exists():
        return False
    
    for guest_product in guest_products:
        user_product = CartProduct.objects.filter(cart=cart, product=guest_product.product).first()

        if user_product:
            user_product.quantity += guest_product.quantity
            user_product.save()
        else:
            guest_product.cart = cart
            guest_product.anonymous_cart = None
            guest_product.save()
    
    anonymous_cart.delete()

    return True