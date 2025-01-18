from django.db import models
from django.contrib.auth.models import User
import hashlib

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    has_used_first_discount = models.BooleanField(default=False)

class DiscountUsage(models.Model):
    email_hash = models.CharField(max_length=64, unique=True)
    discount_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"Discount used: {self.discount_used} for email hash: {self.email_hash}"
    
    @staticmethod
    def hash_email(email):
        return hashlib.sha256(email.encode()).hexdigest()