from django.contrib import admin
from .models import Category, Product, Review, Wishlist, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Tag)