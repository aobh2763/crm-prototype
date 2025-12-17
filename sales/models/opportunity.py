from django.db import models

# Create your models here.
class Opportunity(models.Model):
    class OpportunityStage(models.TextChoices):
        SUSPECTION = 'SU', 'Suspection'
        PROSPECTION = 'PR', 'Prospection'
        ANALYSIS = 'AN', 'Analysis'
        NEGOTIATION = 'NE', 'Negotiation'
        CONTRACTING = 'CO', 'Contracting'
        CLOSED = 'CL', 'Closed'
    
    class OpportunityPriority(models.TextChoices):
        LOW = 'LO', 'Low'
        MEDIUM = 'ME', 'Medium'
        HIGH = 'HI', 'High'
    
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('core.Client', on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=2,
        choices=OpportunityPriority.choices,
        default=OpportunityPriority.MEDIUM
    )
    stage = models.CharField(
        max_length=2,
        choices=OpportunityStage.choices,
        default=OpportunityStage.SUSPECTION
    )
    
    class Meta:
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"
    
    def __str__(self):
        return f"Opportunity {self.id} - {self.get_stage_display()} for {self.client}"
    
    def next_stage(self):
        stage_order = [
            self.OpportunityStage.SUSPECTION,
            self.OpportunityStage.PROSPECTION,
            self.OpportunityStage.ANALYSIS,
            self.OpportunityStage.NEGOTIATION,
            self.OpportunityStage.CONTRACTING,
            self.OpportunityStage.CLOSED
        ]
        
        current_index = stage_order.index(self.stage)
        if current_index < len(stage_order) - 1:
            self.stage = stage_order[current_index + 1]
            self.save()