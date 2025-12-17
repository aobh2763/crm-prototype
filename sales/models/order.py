from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )
    client = models.ForeignKey('core.Client', on_delete=models.CASCADE)

    def calculate_price(self):
        total = sum(line.product.price * line.quantity for line in self.lines.all())
        discount_amount = total * (self.discount / 100)
        return total - discount_amount

    def __str__(self):
        return f"Order {self.id} for {self.client}"


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.quantity} × {self.product.name} in Order {self.order.id}"