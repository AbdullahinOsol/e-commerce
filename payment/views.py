from django.shortcuts import render, redirect
from . models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
import stripe
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from cart.models import CartItem
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):

    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address, 'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY}
            return render(request, 'payment/checkout.html', context=context)
        
        except:
            context = {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY}
            return render(request, 'payment/checkout.html', context=context)

    else:
        context = {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY}
        return render(request, 'payment/checkout.html', context=context)

def payment_success(request):
        
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()

        for key in list(request.session.keys()):
            if key == 'session_key':
                del request.session[key]

        profile = request.user.profile
        profile.has_used_first_discount = True
        profile.save()

        messages.success(request, 'Your order was successfully placed!')
        print('Order placed successfully!')

    return redirect('home')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

def complete_order(request):
    
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode)

        cart = Cart(request)

        cost = cart.get_total()
        total_cost = cost['discounted_total']
        print(total_cost)
        print(type(total_cost))

        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user
                )

        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
            )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                )

        order_success = True
        response = JsonResponse({'success': order_success})
        return response

    return render(request, 'payment/payment-failed.html')
    

def create_checkout_session(request):
    if request.method == 'POST':
        try:    
            cart = Cart(request)
            cost = cart.get_total()
            total_cost = cost['discounted_total']
            # Create Stripe session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Total Order',
                        },
                        'unit_amount': int(total_cost * 100),  # Ensure this line works as expected
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
            )

            return JsonResponse({'id': session.id})  # Ensure that session.id exists
        except Exception as e:
            return JsonResponse({'error': str(e)})