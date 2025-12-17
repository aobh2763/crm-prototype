from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Quantity(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    value = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('product', 'stock')
        ordering = ['product']
    
    def __str__(self):
        return f"{self.value} of {self.product.name}"
    
    def increase(self, amount):
        if amount >= 0:
            self.value += amount
            self.save()
        else:
            raise ValueError("Amount to increase must be non-negative")
    
    def decrease(self, amount):
        if 0 <= amount <= self.value:
            self.value -= amount
            self.save()
        else:
            raise ValueError("Amount to decrease must be non-negative and less than or equal to current quantity")
    
    def is_available(self):
        return self.value > 0