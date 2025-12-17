from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    street = models.CharField(max_length=255, null=False)
    house_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
    
    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}, {self.country}"