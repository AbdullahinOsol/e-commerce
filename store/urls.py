from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.store, name='store'),
    path('', views.home, name='home'),
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle-wishlist'),
    path('wishlist-summary/', views.wishlist_summary, name='wishlist-summary'),
    path('search/', views.search, name='search'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete-review'),
    path('discount-summary/', views.discount_summary, name='discount-summary'),
    path('all-products/', views.all_products, name='all-products'),
]