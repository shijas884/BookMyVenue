from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView
)

from account.permissions import (
    IsCustomerRole,
    IsAdminRole,
    IsOwnerRole
)
from .models import Booking
from account.models import User
from .serializers import (
    BookingListSerializer,
    BookingCreateSerializer,
    BookingCreateSerializer,
    BookingStatusUpdateSerializer,
)


class BookingListCreateView(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer
        return BookingListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomerRole()]
        return [(IsAdminRole | IsOwnerRole | IsCustomerRole)()]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            return Booking.objects.all()

        if user.role == User.Role.CUSTOMER:
            return Booking.objects.filter(customer=user)

        if user.role == User.Role.OWNER:
            return Booking.objects.filter(venue__owner=user)

        return Booking.objects.none()



class BookingStatusUpdateView(UpdateAPIView):
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [IsOwnerRole]
    http_method_names = ["patch"]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.OWNER:
            Booking.objects.filter(
                venue__owner=user
            )
        return Booking.objects.none()