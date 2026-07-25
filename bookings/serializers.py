from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Booking, BookingFacility, BookingService
from venues.models import Facility, Service, Price  


class BookingFacilitySerializer(ModelSerializer):
    class Meta:
        model = BookingFacility
        fields = ["facility", "amount"]


class BookingServiceSerializer(ModelSerializer):
    class Meta:
        model = BookingService
        fields = ["service", "quantity", "amount"]


class BookingListSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "venue",
            "booking_date",
            "start_time",
            "end_time",
            "total_amount",
            "status",
        ]

class BookingCreateSerializer(ModelSerializer):
    price = serializers.PrimaryKeyRelatedField(
        queryset=Price.objects.all(), write_only=True,
    )

    facility_ids = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(), many=True, write_only=True, required=False,
    )

    class ServiceInputSerializer(serializers.Serializer):
        service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
        quantity = serializers.IntegerField(min_value=1)

    services = ServiceInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Booking
        fields = ["venue", "price", "booking_date", "start_time", "end_time", "facility_ids", "services"]

    def validate(self, attrs):
        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError("End time must be after start time.")

        conflict = Booking.objects.filter(
            venue=attrs["venue"],
            booking_date=attrs["booking_date"],
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED],
            start_time__lt=attrs["end_time"],
            end_time__gt=attrs["start_time"],
        ).exists()

        if conflict:
            raise serializers.ValidationError(
                "This venue is already booked for the selected date and time."
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        facilities = validated_data.pop("facility_ids", [])
        services = validated_data.pop("services", [])
        price = validated_data.pop("price")

        booking = Booking.objects.create(
            customer=self.context["request"].user,
            total_amount=price.amount,
            **validated_data,
        )

        total = price.amount

        for facility in facilities:
            BookingFacility.objects.create(booking=booking, facility=facility, amount=facility.amount)
            total += facility.amount

        for item in services:
            BookingService.objects.create(
                booking=booking,
                service=item["service"],
                quantity=item["quantity"],
                amount=item["service"].amount,
            )
            total += item["service"].amount * item["quantity"]

        booking.total_amount = total
        booking.save()

        return booking


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["status"]

