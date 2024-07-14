from django.shortcuts import render, redirect
from .models import Product, CartItem
from .forms import ProductForm, RegistrationForm, OrderForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    products = Product.objects.all()

    try:
        number_of_items = len(CartItem.objects.filter(user=request.user))
    except:
        number_of_items = 0

  

    context = {"products": products, "number_of_items": number_of_items}

    return render(request, "home/home2.html", context)

def about(request):
    number_of_items = request.session.get('number_of_items', 0)
    context = {"number_of_items": number_of_items}
    return render(request, "home/about.html", context)


def details(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    return render(request, "home/details.html", context)

# Create your views here.

@login_required(login_url='user/login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

        
    form = ProductForm()
    context = {"form": form}
    return render(request, "home/add_product.html", context)

def register(request):
    if request.method == "POST":
        user = RegistrationForm(request.POST)
        if user.is_valid():
            user.save()
    
        username = request.POST['username']
        password = request.POST['password1']
        u = authenticate(request, username=username, password=password)

        if u is not None:
            form = login(request, u)
            return redirect('home')
        
    form = RegistrationForm()
    context = {"form": form}
    return render(request, "home/register.html", context)

# @login_required(login_url="login")
# def add_to_cart(request, id):
#     product = Product.objects.get(id=id)
#     cart_item, create = CartItem.objects.get_or_create(product=product, user=request.user)

#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect("home")

@login_required(login_url="login")
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item, create = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.price = product.price * cart_item.quantity
    cart_item.save()

    return redirect("home")

@login_required(login_url="login")
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for i in cart_items:
        total += i.price
    
    number_of_items = len(CartItem.objects.filter(user=request.user))
    
    context = {"cart_items": cart_items, "total_price": total, "number_of_items": number_of_items}
    return render(request, "home/cart.html", context)



@login_required(login_url="login")
def remove_from_cart(request, id):
    cart_item = CartItem.objects.filter(id=id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    form = OrderForm()

    total = 0
    for i in cart_items:
        total += i.price

    context = {"products": cart_items, "total_price": total, "form":form}

    return render(request, "home/checkout.html", context )