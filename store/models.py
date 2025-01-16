from django.db import models
from django.urls import reverse
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.postgres.search import SearchVectorField
from taggit.managers import TaggableManager

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    image_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='un-branded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    category = models.ManyToManyField(Category, related_name='products', blank=True)
    sale = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])
    
    def average_rating(self):
        avg = self.reviews.aggregate(average=Avg('rating'))['average']
        return round(avg, 1) if avg else None
    
    def get_sale_price(self):
        return round(self.price - (self.price * self.sale / 100), 2)
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'reviews'
        ordering = ['-date_added']

    def __str__(self):
        return 'Review - #' + str(self.id)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'wishlist'
        unique_together = ('user', 'product')

    def __str__(self):
        return str(self.product.title) + ' - ' + str(self.user.username)