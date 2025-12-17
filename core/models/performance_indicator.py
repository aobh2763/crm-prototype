from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError

# Create your models here.
class PerformanceIndicator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    target_value = models.FloatField(validators=[MinValueValidator(0.0)])
    actual_value = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    
    def __str__(self):
        return f"Performance Indicator: {self.name} (Target: {self.target_value}, Actual: {self.actual_value})"
    
    def clean(self):
        if self.started_at >= self.ended_at:
            raise ValidationError("Start date must be before end date")