from django.db import models

# Create your models here.
class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    delivery_method = models.CharField(max_length=100)
    
    def total_price(self):
        return self.order.calculate_price()
    
    def __str__(self):
        return f"Sale {self.id} for Order {self.order.id}"