from django.urls import path
from .views import (
    BookingListCreateView,
    BookingStatusUpdateView,
)

urlpatterns = [
    path("bookings/",BookingListCreateView.as_view()),
    path("bookings/<int:pk>/status/",BookingStatusUpdateView.as_view()),
]