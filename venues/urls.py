from django.urls import path

from .views import (
    VenueListCreateView,
    VenueDetailView,
    VenueMediaListCreateView,

)

urlpatterns = [
    path('venues/', VenueListCreateView.as_view()),
    path('venues/<int:pk>/', VenueDetailView.as_view()),
    path('venues/media/', VenueMediaListCreateView.as_view())
  
]