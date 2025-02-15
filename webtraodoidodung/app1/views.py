from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"   
    else:
        items = []
        order = {'get_itemtrade_items': 0, 'get_itemtrade_total': 0}
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','') 
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False)
    context= {'created': created,'products':products,'categories':categories,'items':items,'order':order, 'user_not_login':user_not_login, 'user_login': user_login}
    return render(request, 'app1/detail.html',context)

def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories':categories, 'products':products, 'active_category':active_category}
    return render(request, 'app1/category.html', context) 

def search(request):
    searched = ""  # Đặt giá trị mặc định
    keys = []

    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"

    if request.method == "POST":
        searched = request.POST.get("searched", "")  # Tránh lỗi KeyError
        keys = Product.objects.filter(name__icontains=searched)
    return render(request, 'app1/search.html', {"searched": searched, "keys": keys, 'user_not_login':user_not_login, 'user_login': user_login})

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"

    context = {'form':form, 'user_not_login':user_not_login, 'user_login': user_login}    
    return render(request, 'app1/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        return redirect('home')
    
    else:
        user_not_login = "show"
        user_login = "hidden"

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user )
            return redirect('home')
        else:
            messages.info(request, 'user or password not correct!')

    context = {'user_not_login':user_not_login, 'user_login': user_login}
    return render(request, 'app1/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"       
    else:
        items = []
        order = {'get_itemtrade_items': 0, 'get_itemtrade_total': 0}
        user_not_login = "show"
        user_login = "hidden" 
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    products = Product.objects.all()
    context= {'items':items,'active_category': active_category, 'products': products, 'user_not_login':user_not_login, 'user_login': user_login, 'categories':categories}
    return render(request, 'app1/home.html',context)

def itemtrade(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"   
    else:
        items = []
        order = {'get_itemtrade_items': 0, 'get_itemtrade_total': 0}
        user_not_login = "show"
        user_login = "hidden" 
    categories = Category.objects.filter(is_sub = False)
    context= {'categories':categories,'items':items,'order':order, 'user_not_login':user_not_login, 'user_login': user_login}
    return render(request, 'app1/itemtrade.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"   
    else:
        items = []
        order = {'get_itemtrade_items': 0, 'get_itemtrade_total': 0}
        user_not_login = "show"
        user_login = "hidden" 
    context= {'items':items,'order':order, 'user_not_login':user_not_login, 'user_login': user_login}
    return render(request, 'app1/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
 