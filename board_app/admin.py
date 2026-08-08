from django.contrib import admin

from .models import Board

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display=('title', 'owner')
    search_fields=('title', 'owner__email')