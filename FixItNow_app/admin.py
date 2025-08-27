from django.contrib import admin

# Register your models here.

from .models import UserProfile, Worker, Booking

admin.site.register(UserProfile)
admin.site.register(Worker)
admin.site.register(Booking)