from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book,Order

class BookAdmin(admin.ModelAdmin):
   list_display = [
    'title',
    'author',
    'description',
    'price',
    'stock',
    'image',
]

# class Order:

admin.site.register(Book,BookAdmin)
admin.site.register(Order)
# admin.site.register(OrderItem)


