from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    def __str__(self):
        return f"Subscription {self.name} (ID: {self.id})"