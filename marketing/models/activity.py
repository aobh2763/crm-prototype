from django.db import models

# Create your models here.
class Activity(models.Model):
    class ActivityType(models.TextChoices):
        MEETING = 'ME', 'Meeting'
        CALL = 'CA', 'Call'
        EMAIL = 'EM', 'Email'
        OTHER = 'OT', 'Other'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    activity_type = models.CharField(
        max_length=2,
        choices=ActivityType.choices,
        default=ActivityType.OTHER
    )
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.title} ({self.get_activity_type_display()})"