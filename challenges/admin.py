from django.contrib import admin

from .models import Laptop, Post


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand', 'year', 'ram', 'hdd', 'price', 'quantity',)
    list_filter = ('brand', 'year', 'ram', 'hdd',)
    search_fields = ('brand',)
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'published_at',)
    list_filter = ('author', 'created_at', 'status', )
    search_fields = ('title', 'author', 'status')
    date_hierarchy = 'created_at'
    exclude = ('published_at',)
