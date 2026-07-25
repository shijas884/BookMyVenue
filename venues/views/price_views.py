from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from venues.models import Price
from venues.serializers import PriceSerializer

from account.models import User
from account.permissions import IsOwnerRole, IsAdminRole


class PriceListCreateView(ListCreateAPIView):
    serializer_class = PriceSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOwnerRole()]
        return [(IsAdminRole | IsOwnerRole)()]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return Price.objects.filter(
                venue__owner=user
            )

        return Price.objects.none()


class PriceDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PriceSerializer
    permission_classes = [IsOwnerRole]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return Price.objects.filter(
                venue__owner=user
            )

        return Price.objects.none()