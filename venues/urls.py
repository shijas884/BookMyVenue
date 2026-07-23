from django.urls import path

from venues.views.venues_views import (
    VenueListCreateView,
    VenueDetailView,
    VenueMediaListCreateView,
    VenueMediaDetailView,

)

urlpatterns = [
    path('venues/', VenueListCreateView.as_view()),
    path('venues/<int:pk>/', VenueDetailView.as_view()),
    path('venues/media/', VenueMediaListCreateView.as_view()),
    path('venues/<int:pk>/media/', VenueMediaDetailView.as_view()),

]