from django.db import models

# Create your models here.
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('Product', through='Quantity')
    
    def __str__(self):
        return f"Stock {self.id} with {self.products.count()} products"