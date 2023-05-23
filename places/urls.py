from places.views import ParkView, TopParkView
from django.urls import path

app_label = 'places'
urlpatterns = [
    path('park/<int:pk>/', ParkView.as_view()),
    path('country/<int:pk>/top/', TopParkView.as_view(), name='top_parks')
]
