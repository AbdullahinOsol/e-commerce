from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, default='S')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'cart items'
        unique_together = ('user', 'product')

    def __str__(self):
        return str(self.product.title) + ' - ' + str(self.user.username)
        