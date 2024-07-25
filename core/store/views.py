# from django.shortcuts import render,HttpResponse
# from django.template import loader
from .models import Book,Order,CartItem
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django import forms
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
# from .forms import CustomUserCreationForm
from django.contrib import messages

# from django.contrib.auth import authenticate, login, logout  # Import authentication functions
from django.contrib.auth.decorators import login_required  # Import login_required decorator
# from django.shortcuts import render, redirect
# from django.contrib import messages  # Import messages framework for user feedback


from .models import Book

def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})

def register_view(request):
    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         email = form.cleaned_data.get('email')
    #         password = form.cleaned_data.get('password1')
    #         user = authenticate(email=email, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')
    # else:
        #     form = CustomUserCreationForm()

    if request.method == 'POST':
        first_name= request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username= request.POST.get ('username')
        # first_name=request.POST.get("username")
        password= request.POST.get('password')
        print('fist name and pass',first_name,password)

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'This usrname already taken')
            return redirect('/register/')


        user=User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        )
        user.save()
        # user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'Account created and logged in successfully')
        # messages.info(request,"account created successesfully")
    return render(request, 'signup.html', { })

# def login_view(request):
#     if request.method == 'POST':
#         username= request.POST.get ('username')
#         password= request.POST.get('password')
#         # user=User.objects.filter(username=username)
#         # user=authenticate(request,user)
#         print("username: ",username," and password: ",password)
#         user = authenticate(request, username=username, password=password)
#         # if user.exists():
#         if user is not None:
#             login(request,user)
#             messages.info(request,'Login Succesfully')
#             return redirect('home')
#         else:
#             messages.info(request,'Something goes wrong..please try again')
  

#     return render(request, 'Login.html',{})


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         print("username: ", username, " and password: ", password)
#         user = authenticate(request, username=username, password=password)
#         print( user)

#         if user is not None:
#             print("User is authenticated:", user)
#             login(request, user)
#             messages.info(request, 'Login Successfully')
#             return redirect('home')
#         else:
#             messages.info(request, 'Invalid username or password')
#     return render(request, 'Login.html', {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.info(request, 'Invalid username')
            return render(request, 'Login.html', {})
        
        # Custom logic to compare plain text password with stored password (not recommended)
        if user.password == password:  # This is risky - don't do this
            login(request, user)
            messages.info(request, 'Login Successfully')
            return redirect('home')
        else:
            messages.info(request, 'Invalid password')
            return render(request, 'Login.html', {})
    return render(request, 'Login.html', {})
    



def logout_view(request):
    # logout(request)
    # messages.info(request, 'Logged out successfully')
    logout(request)
    # return HttpResponseRedirect(reverse('home') + '?user=anonymous')
    # return redirect('home')
    return render(request, 'Logout.html',{})



@login_required(login_url='/login/')  # Require login for cart view
def cart_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user).select_related('book')  # Optimize query
    # order=Order.objects.create(user=user)
    # order.user=user
    # order.set(items=cart_items)
    # order.items=cart_item
    # order.set_items(cart_items)
    # order.items.set(cart_items)
    # order.save()

# Check if item already exists in cart for the user
    # existing_item = Cart.objects.filter(user=user, book=book).first()
    # order = Order.objects.filter(user=user).first()
    # order.objects.all().delete()
    # Order.objects.all().delete()
    # if order:
    #     print("order is already",order.user)
    
    # else:
        # order=Order.objects.create(user=user)
        # order.items.set(cart_items)
        # order.save()




    # if existing_item:
    #     existing_item.quantity += 1
    #     existing_item.save()
    #     messages.info(request, f'Quantity of "{book.title}" in cart updated to {user.username}')
    # else:
    #     new_cart_item = CartItem.objects.create(user=user, book=book)
    #     messages.info(request, f'"{book.title}" added to your cart')


    # def get_total_price(self):
    total = 0
    for item in cart_items.all():
        total += item.get_total_price()
    # return total





    context = {'cart_items': cart_items,'cart_total':total}
    # context = {'cart_items': cart_items,'cart_total':500}

    return render(request, 'cart.html', context)


@login_required(login_url='/login/')  # Require login for add_to_cart
def add_to_cart(request, book_id):
    user = request.user

    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        messages.info(request, 'Book not found')
        return redirect('home')

    # Check if item already exists in cart for the user
    # existing_item = Cart.objects.filter(user=user, book=book).first()
    existing_item = CartItem.objects.filter(user=user, book=book).first()


    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
        messages.info(request, f'Quantity of "{book.title}" in cart updated to {user.username}')
    else:
        new_cart_item = CartItem.objects.create(user=user, book=book)
        messages.info(request, f'"{book.title}" added to your cart')

    return redirect('home')  # Redirect back to the home page



# @login_required(login_url='/login/')  # Require login for add_to_cart
# def remove_from_cart(request, book_id):
#     user = request.user

#     try:
#         book = Book.objects.get(pk=book_id)
#     except Book.DoesNotExist:
#         messages.info(request, 'Book not found')
#         return redirect('home')

#     # Check if item already exists in cart for the user
#     # existing_item = Cart.objects.filter(user=user, book=book).first()
#     existing_item = CartItem.objects.filter(user=user, book=book).first()
#     existing_item.delete()
#     print("delted: ",existing_item)

#     return redirect('cart')  # Redirect back to the home page


@login_required(login_url='/login/')  # Require login for add_to_cart
def remove_from_cart(request, book_id):
    user = request.user

    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        messages.info(request, 'Book not found')
        return redirect('home')

    # Find the CartItem object for the user and book
    existing_item = CartItem.objects.filter(user=user, book=book).first()

    if existing_item:
        existing_item.delete()
        # messages.info(request, f'"{book.title}" removed from your cart')
        print(request, f'"{book.title}" removed from your cart')

    else:
        # messages.info(request, f'"{book.title}" not in your cart')
        print(request, f'"{book.title}" not in your cart')


    return redirect('cart')  # Redirect back to the cart page



@login_required(login_url='/login/')  # Require login for add_to_cart
def checkout(request):
    user = request.user
    item=CartItem.objects.filter(user=user)
    if item:
        print("item exist: ",item)
    else:
        print("item is not present",item)
    # item=request.cart_item
    # try:
    #     book = Book.objects.get(pk=book_id)
    # except Book.DoesNotExist:
    #     messages.info(request, 'Book not found')
    #     return redirect('home')

    # Check if item already exists in cart for the user
    # existing_item = Cart.objects.filter(user=user, book=book).first()
    # items = CartItem.objects.filter(user=user, book=book).first()
    try:
        order=Order.objects.create(user=user )
        order.items.set(item)
        order.save()
        item.delete()
        return redirect(request,'checkout.html')
    except Exception as e:
        print(e)
        return redirect('home')


def search(request):
    query = request.GET.get('search')  
    if query:
        books = Book.objects.filter(title__icontains=query)  
    else:
        books = []  
    return render(request, 'search_results.html', {'books': books})
