from django.contrib import admin
from .models import Book, Category
# Register your models here.

class BookInline(admin.TabularInline):
    model =  Book 

class CatgoryAdmin(admin.ModelAdmin):
    inlines = [
        BookInline
    ]

class BookAdmin(admin.ModelAdmin):
    list_display = [
        'name','author','desc','image'
    ]
    list_filter = [
        'date_added','name'
    ]
    sortable_by = [
        'author', 'category', 'genre'
    ]

admin.site.register(Book, BookAdmin)
admin.site.register(Category, CatgoryAdmin)