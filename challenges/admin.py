from django.contrib import admin

from .models import Laptop


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand', 'year', 'ram', 'hdd', 'price', 'quantity',)
    list_filter = ('brand', 'year', 'ram', 'hdd',)
    search_fields = ('brand',)
    date_hierarchy = 'created_at'
