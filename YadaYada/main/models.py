from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class LocalUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

class Booking(models.Model):
    user = models.ForeignKey(LocalUser, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.destination} ({self.checkin} to {self.checkout})"
