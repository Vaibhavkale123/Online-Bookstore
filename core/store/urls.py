from django.contrib import admin
from django.urls import path
from  . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home,name='home'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    # path('register/', views.signup),
    path('register/', views.register_view),
    path('cart/', views.cart_view,name='cart'),
    # path('checkout/', views.checkout,name='checkout'),
    path('add-to-cart/<int:book_id>', views.add_to_cart),
    path('remove-from-cart/<int:book_id>', views.remove_from_cart,name='remove_from_cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('search/', views.search, name='search'),
    path('book/<int:book_id>', views.book, name='book'),










]
