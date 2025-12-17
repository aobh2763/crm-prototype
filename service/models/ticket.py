from django.db import models

# Create your models here.
class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        OPEN = 'OP', 'Open'
        IN_PROGRESS = 'IP', 'In Progress'
        RESOLVED = 'RE', 'Resolved'
        CLOSED = 'CL', 'Closed'
    
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=2,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Ticket {self.id} - {self.subject} ({self.get_status_display()})"