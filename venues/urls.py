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
from venues.views.service_views import (
    ServiceListCreateView,
    ServiceDetailView,
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

    # Services
    path("services/",ServiceListCreateView.as_view()),
    path("services/<int:pk>/",ServiceDetailView.as_view()),
]
