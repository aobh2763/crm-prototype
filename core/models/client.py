from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='clients')
    subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL, null=True, blank=True, related_name='clients')
    
    def __str__(self):
        return f"Client {self.name} (ID: {self.id})"