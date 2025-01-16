from django.shortcuts import render
from . cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CartItem
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)
        
        cart_quantity = cart.__len__()
        total = cart.get_total()
        cart_total = total['discounted_total']
        cart_total_before_discount = total['original_total']

        cart_items = [
            {
                'title': item['product'].title,
                'qty': item['qty'],
                'price': float(item['price']),
                'discounted_price': str(item['product'].get_sale_price()),
                'total': float(item['total']),
                'description': item['product'].description,
            }
            for item in cart
        ]
        
        print(cart_items)
        response = JsonResponse({'qty': cart_quantity, 'total': float(cart_total), 'items': cart_items, 'total_before_discount': float(cart_total_before_discount)})
        return response

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})
        return response

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product=product_id, qty=product_quantity)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response

def synchronize_cart_from_db(request):
    if request.user.is_authenticated:
        cart = Cart(request)

        # Fetch items from the user's database cart
        user_cart_items = CartItem.objects.filter(user=request.user)
        session_cart = request.session.get('session_key', {})

        # Step 1: Merge the session cart with the database cart
        for item in user_cart_items:
            product = item.product
            product_id_str = str(product.id)

            if product_id_str in session_cart:
                # Compare quantities: session vs. database
                session_quantity = int(session_cart[product_id_str]['qty'])
                db_quantity = item.quantity

                # Use the higher quantity and update both the session and database
                higher_quantity = max(session_quantity, db_quantity)
                cart.add(product, higher_quantity)  # This method updates both session and DB
            else:
                # If the product is only in the DB, add it to the session
                cart.add(product, item.quantity)

        # Step 2: Add session items to the database if they are not already present
        for product_id_str, session_data in session_cart.items():
            product_id = int(product_id_str)
            product = get_object_or_404(Product, id=product_id)

            # Check if the product exists in the user's database cart
            try:
                db_item = CartItem.objects.get(user=request.user, product=product)
                # If the item exists, it's already handled in the previous loop
            except CartItem.DoesNotExist:
                # If the product is only in the session, add it to the database
                cart.add(product, int(session_data['qty']))

        # At the end, ensure the session is properly updated and saved
        request.session['session_key'] = cart.cart

@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):
    synchronize_cart_from_db(request)