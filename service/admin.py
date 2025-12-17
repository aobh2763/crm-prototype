from django.contrib import admin

from .export_strategies import export_with_strategy, CSVStrategy, ExcelStrategy, PDFStrategy
from .models import Ticket, Article

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('subject', 'description')
    ordering = ('-created_at',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_at', 'created_at', 'updated_at')
    list_filter = ('published_at', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    
    actions = [
        export_with_strategy(CSVStrategy),
        export_with_strategy(ExcelStrategy),
        export_with_strategy(PDFStrategy),
    ]