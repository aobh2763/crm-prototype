import uuid
from django.db import models

# Create your models here.
class Bill(models.Model):
    class InvoiceType(models.TextChoices):
        STANDARD = 'ST', 'Standard'
        DEBIT = 'DE', 'Debit'
        CREDIT = 'CR', 'Credit'
        PROFORMA = 'PR', 'Proforma'
        
    reference = models.CharField(
        max_length=12,
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4().hex[:12]
    )
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    invoice_type = models.CharField(
        max_length=2,
        choices=InvoiceType.choices,
        default=InvoiceType.STANDARD
    )
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Bill {self.reference} - {self.get_invoice_type_display()}"