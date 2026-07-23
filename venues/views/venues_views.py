from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,

)
from rest_framework.parsers import MultiPartParser, FormParser


from venues.serializers import (
    VenueCreateSerializer,
    VenueListSerializer,
    VenueAdminUpdateSerializer,
    VenueOwnerUpdateSerializer,
    VenueMediaSerializer,
)
from venues.models import Venue, VenueMedia
from account.models import User
from account.permissions import IsOwnerRole, IsAdminRole

# Create your views here.


class VenueListCreateView(ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOwnerRole()]
        return [(IsOwnerRole | IsAdminRole)()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return VenueCreateSerializer
        return VenueListSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            return Venue.objects.all()

        if user.role == User.Role.OWNER:
            return Venue.objects.filter(owner=user)

        return Venue.objects.none


class VenueDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminRole | IsOwnerRole]

    def get_serializer_class(self):
        if self.request.user.role == User.Role.ADMIN:
            return VenueAdminUpdateSerializer
        return VenueOwnerUpdateSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            return Venue.objects.all()

        if user.role == User.Role.OWNER:
            return Venue.objects.filter(owner=user)

        return Venue.objects.none
    
class VenueMediaListCreateView(ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = VenueMediaSerializer
    permission_classes = [IsOwnerRole]
    
    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return VenueMedia.objects.filter(venue__owner=user)

        return VenueMedia.objects.none

class VenueMediaDetailView(RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = VenueMediaSerializer
    permission_classes = [IsOwnerRole]
    
    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.OWNER:
            return VenueMedia.objects.filter(venue__owner=user)

        return VenueMedia.objects.none

