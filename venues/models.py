from django.db import models
from account.models import User
from locations.models import District, State


# Create your models here.
class Venue(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="venues",
    )

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    state = models.ForeignKey(State, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    hall_capacity = models.PositiveIntegerField()
    dining_capacity = models.PositiveIntegerField(default=0)

    car_parking_capacity = models.PositiveIntegerField(default=0)
    bike_parking_capacity = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VenueMedia(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="venue_media",
        null=True,
        blank=True,
    )
    file = models.FileField(upload_to="venues/")


class Facility(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="facilities",
    )
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "name"],
                name="unique_facility_per_venue",
            )
        ]

    def __str__(self):
        return self.name


class Service(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="services",
    )
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10,decimal_places=2,)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "name"],
                name="unique_service_per_venue",
            )
        ]

    def __str__(self):
        return self.name


class Price(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="prices",
    )

    name = models.CharField(max_length=100)

    amount = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "name"],
                name="unique_price_per_venue",
            )
        ]

    def __str__(self):
        return f"{self.venue.name} - {self.name}"
