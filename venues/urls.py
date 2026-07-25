from django.urls import path

from venues.views.venues_views import (
    VenueListCreateView,
    VenueDetailView,
    VenueMediaListCreateView,
    VenueMediaDetailView,

)
from venues.views.facility_views import (
    FacilityListCreateView,
    FacilityDetailView,
)

urlpatterns = [
    # Venue
    path("venues/", VenueListCreateView.as_view()),
    path("venues/<int:pk>/", VenueDetailView.as_view()),

    # Venue Media
    path("venue-media/", VenueMediaListCreateView.as_view()),
    path("venue-media/<int:pk>/", VenueMediaDetailView.as_view()),

    # Facility
    path("facilities/", FacilityListCreateView.as_view()),
    path("facilities/<int:pk>/", FacilityDetailView.as_view()),
]
