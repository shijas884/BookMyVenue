from django.db import models
from account.models import User
from venues.models import Venue, Facility, Service

# Create your models here.

class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings",)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE,related_name="bookings",)

    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.venue}"


class BookingFacility(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="selected_facilities",
    )

    facility = models.ForeignKey(Facility,on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.booking} - {self.facility}"


class BookingService(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="selected_services",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.booking} - {self.service}"
    
    
