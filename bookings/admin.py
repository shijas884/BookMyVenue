from django.contrib import admin

from  .models import Booking,BookingFacility,BookingService
# Register your models here.

admin.site.register(Booking)
admin.site.register(BookingFacility)
admin.site.register(BookingService)

