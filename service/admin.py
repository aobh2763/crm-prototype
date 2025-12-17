from django.contrib import admin
from .models import Ticket, Article

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('subject', 'description')
    ordering = ('-created_at',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_at', 'created_at', 'updated_at')
    list_filter = ('published_at', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)