from django.shortcuts import render, redirect
from .models import Product, CartItem
from .forms import ProductForm, RegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "home/home2.html", context)

def about(request):
    return render(request, "home/about.html")


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
    context = {"cart_items": cart_items, "total_price": total}
    return render(request, "home/cart.html", context)


# def remove_from_cart(request, id):
#     cart_item = CartItem.objects.filter(id=id)
#     cart_item.delete()
#     return redirect('view_cart')


@login_required(login_url="login")
def remove_from_cart(request, id):
    cart_item = CartItem.objects.filter(id=id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')