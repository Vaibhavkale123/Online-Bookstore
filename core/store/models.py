from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image=models.ImageField(upload_to='book_cover/',default='book_cover/blog.jpg')
  


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Default quantity to 1

    def get_total_price(self):
        return self.quantity * self.book.price

    

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE,default=None)
#     orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE,default=None)
#     created_at = models.DateTimeField(auto_now_add=True)



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(CartItem)  # Many-to-Many relationship with CartItem

    # def set_items(self,item):
    #     self.items=item
        

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_total_price()
        return total
