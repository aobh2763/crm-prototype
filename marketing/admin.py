from django.contrib import admin

from sales.models.opportunity import Opportunity

from .export_strategies import export_with_strategy, CSVStrategy, ExcelStrategy, PDFStrategy
from .models import Activity, Campaign, Contact, Prospect

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'activity_type', 'date', 'created_at')
    search_fields = ('title', 'description', 'activity_type')
    list_filter = ('activity_type', 'date')
    ordering = ('-date',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'budget', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

@admin.action(description="Qualify selected prospects into opportunities")
def qualify_prospects(modeladmin, request, queryset):
    for prospect in queryset:
        if prospect.client:
            Opportunity.objects.create(
                client=prospect.client,
                priority=Opportunity.OpportunityPriority.MEDIUM,
                stage=Opportunity.OpportunityStage.SUSPECTION
            )
        
        prospect.is_active = False
        prospect.save()
        
@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'is_active')
    ordering = ('-created_at',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
        qualify_prospects
    ]
