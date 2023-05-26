from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db.models import Avg

from store.models import Profile, Review

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Review)
def product_rate_calculator(sender, instance, **kwargs):
    
    product = instance.product
    avarage_rate = Review.objects.filter(product=product).aggregate(Avg("rate"))['rate__avg']
    product.avarage_rate = avarage_rate
    product.save()