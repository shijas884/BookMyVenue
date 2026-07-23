from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from .models import Venue,Service,Facility,Price,VenueMedia


class ServiceSerializer(ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'

class FacilitySerializer(ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'

class VenueMediaSerializer(ModelSerializer):

    class Meta:
        model = VenueMedia
        fields = ["id","file","venue"]

class PriceSerializer(ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'



class VenueCreateSerializer(ModelSerializer):
    media_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False)
    class Meta:
        model = Venue
        fields = [
            "id",
            "name",
            "description",
            "address_line",
            "city",
            "pincode",
            "state",
            "district",
            "media_ids"
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        media_ids =validated_data.pop("media_ids",[])
        validated_data['owner'] = user

        venue = Venue.objects.create(**validated_data)
        VenueMedia.objects.filter(
            id__in=media_ids,
            venue__isnull=True

        ).update(venue=venue)
        return venue
    
class VenueListSerializer(ModelSerializer):
    venue_media = VenueMediaSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Venue
        fields = [
            "name",
            "description",
            "address_line",
            "city",
            "pincode",
            "state",
            "district",
            "venue_media",
            "status",
        ]

class VenueOwnerUpdateSerializer(ModelSerializer):
      class Meta:
            model = Venue
            fields = [
                "description",
                "address_line",
                "city",
                "pincode",
                "state",
                "district",
            ]
class VenueAdminUpdateSerializer(ModelSerializer):
       class Meta:
        model = Venue
        fields = ["id","status"]
        


