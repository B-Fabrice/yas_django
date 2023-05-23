from django.db import models
from django.dispatch import receiver
from django.core.cache import cache

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Park(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
    park = models.ForeignKey(Park, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=255, blank=True, null=True)

@receiver(models.signals.post_delete, sender=Photo)
@receiver(models.signals.post_save, sender=Photo)
def delete_cached_photos(sender, instance, **kwargs):
    photos_cache_key = f'photos-{instance.park.id}'
    cache.delete(photos_cache_key)