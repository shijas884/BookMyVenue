from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from venues.models import Service
from venues.serializers import ServiceSerializer

from account.models import User
from account.permissions import IsOwnerRole, IsAdminRole


class ServiceListCreateView(ListCreateAPIView):
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
            if self.request.method == "POST":
                return [IsOwnerRole()]
            return [(IsAdminRole | IsOwnerRole)]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return Service.objects.filter(
                venue__owner=user
            )

        return Service.objects.none()


class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsOwnerRole]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return Service.objects.filter(
                venue__owner=user
            )

        return Service.objects.none()