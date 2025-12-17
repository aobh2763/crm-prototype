from django.contrib import admin

from .export_strategies import export_with_strategy, CSVStrategy, ExcelStrategy, PDFStrategy
from .models import Product, Stock, Quantity, Client, Subscription, Address

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

class QuantityInline(admin.TabularInline):
    model = Quantity
    extra = 1

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_count')
    inlines = [QuantityInline]
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

    def product_count(self, obj):
        return obj.quantity_set.count()

    product_count.short_description = 'Number of Products'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'subscription', 'is_active', 'joined_at')
    list_filter = ('is_active', 'subscription')
    search_fields = ('name', 'email', 'phone_number')
    ordering = ('-joined_at',)
    autocomplete_fields = ('address', 'subscription')
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'discount')
    search_fields = ('name',)
    ordering = ('name',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street', 'house_number', 'postal_code', 'city', 'country')
    search_fields = ('street', 'city', 'country', 'postal_code')
    ordering = ('country', 'city', 'street')
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]
