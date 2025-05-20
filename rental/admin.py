# Register your models here.
from django.contrib import admin
from .models import Car, Booking, Profile

admin.site.register(Car)
admin.site.register(Booking)
admin.site.register(Profile)