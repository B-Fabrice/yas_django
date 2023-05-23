from places.models import Park, Country
from django.views.generic import TemplateView
from django.core.cache import cache
from django.db.models import Avg

class ParkView(TemplateView):
    template_name = 'places/park.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        park_id = self.kwargs['pk']
        photo_cache_key = f'photos-{park_id}'
        photos = cache.get(photo_cache_key)
        review_cache_key = cache.get(f'reviews-{park_id}')
        reviews = cache.get(review_cache_key)

        if not photos:
            park = Park.objects.get(id=park_id)
            photos = park.photos.all()
            cache.set(photo_cache_key, photos)

        if not reviews:
            park = Park.objects.get(id=park_id)
            reviews = park.reviews.all()
            cache.set(review_cache_key, photos)

        context['photos'] = photos
        context['reviews'] = reviews
        context['park'] = Park.objects.get(pk=kwargs['pk'])
        return context

class TopParkView(TemplateView):
    template_name = 'places/top_parks.html'
    
    def get_context_data(self, **kwargs):
        country_id = self.kwargs['pk']
        parks_cache_key = f'parks-{country_id}'
        parks = cache.get(parks_cache_key)

        if not parks:
            parks = Park.objects.filter(country=country_id).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:10]
            cache.set(parks_cache_key, parks)

        context = super().get_context_data(**kwargs)
        context['country'] = Country.objects.get(pk=country_id)
        context['parks'] = parks
        return context