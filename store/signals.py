from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
import random

@receiver(post_save, sender=Product)
def update_category_image(sender, instance, **kwargs):
    print('Signal Triggered')
    for category in instance.category.all():
        print(category.name)
        first_product = category.products.order_by('?').first()
        print(first_product.title)

        if first_product and first_product.image:
            print(first_product.image.url)
            category.image_name = first_product.image.url
            category.save()
            print(category.image_name)