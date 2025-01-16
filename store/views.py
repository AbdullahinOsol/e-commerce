from cart.cart import Cart
from django.urls import reverse
from django.db.models import Count
from payment.models import OrderItem
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector
from . models import Category, Product, Review, Wishlist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

def store(request):
    all_products = Product.objects.all()
    context = {'all_products': all_products}

    return render(request, 'store/store.html', context=context)

def categories(request):
    all_categories = Category.objects.all()

    return {'all_categories': all_categories}

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    star_range = range(1, 6)

    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        products = annotate_wishlist_status(products, user_wishlist)

    return render(request, 'store/list-category.html', {'category': category, 'products': products, 'star_range': star_range})

def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    reviews = Review.objects.filter(product=product)

    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(user=request.user, product=product).exists()
        has_commented = Review.objects.filter(user=request.user, product=product).exists()
        has_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    else:
        has_purchased = False
        has_commented = False
        has_wishlist = False

    context = {'product': product, 'reviews': reviews, 'has_purchased': has_purchased, 'has_commented': has_commented, 'has_wishlist': has_wishlist}

    if request.method == 'POST':
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if rating and content:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                content=content,
                image=image,
            )

            return redirect(reverse('product-info', args=[product_slug]))

    return render(request, 'store/product-info.html', context=context)

def toggle_wishlist(request):
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        test_string = request.POST.get('test_string')
        product = get_object_or_404(Product, id=product_id)
        
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            action = 'removed'

        else:
            action = 'added'

        print('toggle-wishlist is performed')
        print(test_string)

        return JsonResponse({'action': action})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def wishlist_summary(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    products_in_wishlist = [item.product for item in wishlist_items]

    user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    products_in_wishlist = annotate_wishlist_status(products_in_wishlist, user_wishlist)
    star_range = range(1, 6)

    context = {'products': products_in_wishlist, 'star_range': star_range}
    return render(request, 'store/wishlist-summary.html', context=context)

def annotate_wishlist_status(queryset, user_wishlist):
    """
    Annotate each product in the queryset with the 'in_wishlist' attribute.
    """
    for product in queryset:
        product.in_wishlist = product.id in user_wishlist
    return queryset

#@login_required(login_url='my-login')
def home(request):
    cart = Cart(request)
    categories = Category.objects.all()
    products = Product.objects.all()[:10]
    popular_products = Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count')[:10]
    recent_products = Product.objects.all().order_by('-date_added')[:10]
    star_range = range(1, 6)

    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        products = annotate_wishlist_status(products, user_wishlist)
        popular_products = annotate_wishlist_status(popular_products, user_wishlist)
        recent_products = annotate_wishlist_status(recent_products, user_wishlist)
    
    context = {'categories': categories, 'cart': cart, 'products': products, 'star_range': star_range, 'popular_products': popular_products, 'recent_products': recent_products}
    return render(request, 'store/index.html', context=context)

def search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    if query:
        products_by_title_or_brand = Product.objects.annotate(
            search=SearchVector('title', 'brand')
        ).filter(
            search=query
        ).distinct()

        products_by_tags = Product.objects.filter(
            tags__name__icontains=query
        ).distinct()

        products = (products_by_title_or_brand | products_by_tags).distinct()
        
    else:
        products = Product.objects.none()

    if category_id:
        products = products.filter(category__id=category_id)

    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        products = annotate_wishlist_status(products, user_wishlist)
    star_range = range(1, 6)

    return render(request, 'store/list-category.html', {'query': query, 'products': products, 'star_range': star_range, 'category_id': category_id})


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()

    return JsonResponse({'message': 'Review deleted successfully'})

def discount_summary(request):
    discounted_products = Product.objects.filter(sale__gt=0)
    heading = 'Discounted Products'
    star_range = range(1, 6)

    return render(request, 'store/list-category.html', {'heading': heading, 'products': discounted_products, 'star_range': star_range})