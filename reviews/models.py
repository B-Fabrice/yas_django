from django.db import models
from django.dispatch import receiver
from django.core.cache import cache
from places.models import Park
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Review(models.Model):
    park = models.ForeignKey(Park, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(models.signals.post_delete, sender=Review)
@receiver(models.signals.post_save, sender=Review)
def delete_cached_reviews(sender, instance, **kwargs):
    review_cache_key = f'reviews-{instance.park.id}'
    country_cache_key = f'parks-{instance.park.country.id}'
    cache.delete(review_cache_key)
    cache.delete(country_cache_key)