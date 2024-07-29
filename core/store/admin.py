# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from .models import Book,Order,CartItem

# class BookAdmin(admin.ModelAdmin):
#    list_display = [
#     'title',
#     'author',
#     'description',
#     'price',
#     'stock',
#     'image',
# ]


# # class OrderAdmin(admin.ModelAdmin):

# #     list_display = ('id', 'user_name', 'order_date', 'total_price')
# #     inlines = [OrderItemInline]

# #     def user_name(self, obj):
# #         return obj.user.username

# #     def order_date(self, obj):
# #         return obj.created_at

# #     def total_price(self, obj):
# #         return obj.total_price

# #    list_display = [
# #     'user_id',
# #     'items',
   
# # ]
#     # list_display = ('id', 'user', 'get_total_price', 'created_at')

#     # def get_total_price(self, obj):
#     #     return obj.quantity

#     # get_total_price.short_description = 'Total Price'

# #   list_display = ('id', 'user', 'total_price', 'created_at')

# # class Order:



# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 0
#     readonly_fields = ('book_name', 'quantity', 'total_price')

#     def book_name(self, obj):
#         return obj.book.title

#     def total_price(self, obj):
#         return obj.get_total_price()

# # class OrderAdmin(admin.ModelAdmin):
#     #     list_display = ('id', 'user_name', 'order_date', 'total_price')
# #     inlines = [CartItemInline]

# #     def user_name(self, obj):
# #         return obj.user.username

# #     def order_date(self, obj):
# #         return obj.created_at

# #     def total_price(self, obj):
# #         return obj.get_total_price()

# class OrderItemInline(admin.TabularInline):
#     model = CartItem
#     readonly_fields = ('book', 'quantity', 'get_total_price')
#     extra = 0  # Set to 0 to disable the ability to add new inline items


# class OrderAdmin(admin.ModelAdmin):
#     list_display = [
#         'user_name',
#         'order_date',
#         'get_total_price',
#     ]
#     inlines = [OrderItemInline]

#     def user_name(self, obj):
#         return obj.user.username

#     user_name.short_description = 'User Name'

#     def order_date(self, obj):
#         return obj.created_at.strftime('%Y-%m-%d')

#     order_date.short_description = 'Order Date'

#     def get_total_price(self, obj):
#         return obj.get_total_price()

# # admin.site.register(Book)
# # admin.site.register(Order, OrderAdmin)


# admin.site.register(Book,BookAdmin)
# admin.site.register(Order,OrderAdmin)
# # admin.site.register(OrderItem)


from django.contrib import admin
from .models import Book, Order, CartItem

class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'description',
        'price',
        'stock',
        'image',
    ]

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('book_name', 'quantity', 'total_price')

    def book_name(self, obj):
        return obj.book.title

    def total_price(self, obj):
        return obj.get_total_price()

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user_name',
        'order_date',
        'get_books',
        'get_quantities',
        # 'get_total_price',
    ]
    inlines = [CartItemInline]

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = 'User Name'

    def order_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')

    order_date.short_description = 'Order Date'

    def get_books(self, obj):
        return ", ".join([item.book.title for item in obj.items.all()])

    get_books.short_description = 'Books'

    def get_quantities(self, obj):
        return ", ".join([str(item.quantity) for item in obj.items.all()])

    get_quantities.short_description = 'Quantities'

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'

admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)
