from django.db import models

# Create your models here.
# models.py

from django.contrib.auth.models import User

# Extend Django's User model for admin and worker roles
class UserProfile(models.Model):
    USER_ROLES = (
        ('user', 'User'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')

    def __str__(self):
        return f" name: {self.user}, role :{self.role}"

# Worker-specific details
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(null=True)
    worker_type = models.CharField(max_length=100) # e.g., 'Plumber', 'Electrician'
    about = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    contact_number = models.CharField(max_length=15)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

# Booking request model
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='requests')
    booking_date = models.DateField()
    booking_time = models.TimeField(null=True)
    address = models.TextField(max_length=255,null=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.worker} by {self.user}"