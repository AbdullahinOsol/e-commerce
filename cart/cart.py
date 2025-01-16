from decimal import Decimal
from store.models import Product
import copy
from . models import CartItem

class Cart():

    def __init__(self, request):
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        self.session.modified = True

        if self.user:
            cart_item, created = CartItem.objects.get_or_create(user=self.user, product=product)
            cart_item.quantity = product_qty
            cart_item.save()

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.user:
            CartItem.objects.filter(user=self.user, product_id=product_id).delete()

    def update(self, product, qty):
        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity

        self.session.modified = True

        if self.user:
            cart_item = CartItem.objects.get(user=self.user, product=product)
            cart_item.quantity = qty
            cart_item.save()

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product'] = product
            sale_price = product.get_sale_price()
            cart[str(product.id)]['discounted_price'] = sale_price
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            item['discounted_total'] = Decimal(item['discounted_price']) * item['qty']
            yield item

    def get_total(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        total = 0

        for product in products:
            product_id = str(product.id)
            if product_id in self.cart:
                quantity = self.cart[product_id]['qty']
                sale_price = product.get_sale_price()
                total += Decimal(sale_price) * quantity

        discounted_total = total
        if self.user and self.user.is_authenticated:
            if not self.user.profile.has_used_first_discount:
                discounted_total = total * Decimal(0.75)
                discounted_total = round(discounted_total, 2)

        return {
            'original_total': total,
            'discounted_total': discounted_total
        }
    
    def get_unique_product_count(self):
        return len(self.cart)