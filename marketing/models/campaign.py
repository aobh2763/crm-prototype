from django.db import models
from django.forms import ValidationError

# Create your models here.
class Campaign(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")