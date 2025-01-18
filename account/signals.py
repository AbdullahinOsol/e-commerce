from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, DiscountUsage

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        email_hash = DiscountUsage.hash_email(instance.email)

        if DiscountUsage.objects.filter(email_hash=email_hash, discount_used=True).exists():
            profile.has_used_first_discount = True
            profile.save()