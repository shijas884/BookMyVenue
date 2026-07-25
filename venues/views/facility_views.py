from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from venues.models import Facility
from venues.serializers import FacilitySerializer

from account.permissions import IsOwnerRole, IsAdminRole
from account.models import User


class FacilityListCreateView(ListCreateAPIView):
    serializer_class = FacilitySerializer


    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOwnerRole()]
        return [(IsAdminRole | IsOwnerRole)()]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return Facility.objects.filter(
                venue__owner=user
            )

        return Facility.objects.none()


class FacilityDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FacilitySerializer
    permission_classes = [IsOwnerRole]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return Facility.objects.filter(
                venue__owner=user
            )

        return Facility.objects.none()