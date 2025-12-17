from django.contrib import admin

from .export_strategies import export_with_strategy, CSVStrategy, ExcelStrategy, PDFStrategy
from .models import Bill, Opportunity, Order, Sale, OrderLine

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('reference', 'sale', 'invoice_type', 'is_approved', 'is_paid')
    search_fields = ('reference',)
    list_filter = ('invoice_type', 'is_approved', 'is_paid')
    ordering = ('-reference',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'priority', 'stage')
    search_fields = ('client__name',)
    list_filter = ('priority', 'stage')
    ordering = ('-id',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
        'advance_stage'
    ]

    def advance_stage(self, request, queryset):
        for opportunity in queryset:
            opportunity.next_stage()
        self.message_user(request, f"{queryset.count()} opportunity(ies) advanced to the next stage.")
    advance_stage.short_description = "Move selected opportunities to next stage"

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'discount', 'total_price_display')
    search_fields = ('client__name',)
    list_filter = ('discount',)
    ordering = ('-id',)
    inlines = [OrderLineInline]

    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

    def total_price_display(self, obj):
        return obj.calculate_price()
    total_price_display.short_description = "Total Price"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'sale_date', 'delivery_method', 'total_price_display')
    search_fields = ('order__client__name',)
    list_filter = ('sale_date', 'delivery_method')
    ordering = ('-sale_date',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "Total Price"