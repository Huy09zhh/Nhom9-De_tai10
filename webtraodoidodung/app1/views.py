from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.conf import settings  # Thêm dòng này
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def product_create(request, slug=None):
    categories = Category.objects.all()  # Lấy toàn bộ danh mục

    if request.method == "POST":
        category_ids = request.POST.getlist('category')  # Lấy danh sách danh mục từ form
        name = request.POST.get('name', '')
        price = request.POST.get('price', 0)
        image = request.FILES.get('image', None)
        detail = request.POST.get('detail', '')
        digital = request.POST.get('digital', 'false') == 'true'  # Chuyển từ chuỗi sang boolean
        stock_quantity = request.POST.get('stock_quantity', '0')
        sold_quantity = request.POST.get('sold_quantity', '0')


        # Tạo sản phẩm
        item_product = Product(stock_quantity=stock_quantity,sold_quantity=sold_quantity,name=name, price=price, image=image, digital=digital, detail=detail)
        item_product.save()

        # Gán danh mục
        if category_ids:
            item_product.category.set(Category.objects.filter(id__in=category_ids))

        messages.success(request, 'Sản phẩm được tạo thành công!')

        return redirect('/product_list/')

    return render(request, 'app1/product_create.html', {'categories': categories})

def product_list(request):
    items_product = Product.objects.all()

    total_revenue =  sum(product.price * product.sold_quantity for product in items_product)

    return render(request, 'app1/product_list.html', {
        "items_product": items_product,
        "total_revenue": total_revenue
    })

def product_update(request, product_id):
    item_product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == "POST":
        category_ids = request.POST.getlist('category')  
        item_product.name = request.POST.get('name', item_product.name)
        item_product.price = request.POST.get('price', item_product.price)
        item_product.detail = request.POST.get('detail', item_product.detail)
        item_product.digital = request.POST.get('digital', 'false') == 'true'
        item_product.stock_quantity = request.POST.get('stock_quantity', item_product.stock_quantity)
        item_product.sold_quantity = request.POST.get('sold_quantity', item_product.sold_quantity)

        # Cập nhật hình ảnh nếu có
        if 'image' in request.FILES:
            item_product.image = request.FILES['image']

        # Lưu sản phẩm đã chỉnh sửa
        item_product.save()

        # Cập nhật danh mục sản phẩm
        if category_ids:
            item_product.category.set(Category.objects.filter(id__in=category_ids))

        messages.success(request, 'Sản phẩm được cập nhật thành công!')
        
        return redirect('/product_list/')

    return render(request, 'app1/product_update.html', {'item_product': item_product, 'categories': categories})

def product_delete(request, product_id):
    item_product = Product.objects.get(id=product_id)

    # Xóa hình ảnh
    if item_product.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(item_product.image))
        if os.path.exists(image_path):  # Kiểm tra file có tồn tại không
            os.remove(image_path)  # Xóa file ảnh

    item_product.delete()
    messages.success(request, 'Sản phẩm được xóa thành công!')
    return redirect('/product_list/')

def detail(request):

    OrderItem.objects.filter(product=None).delete()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"   
    else:
        items = []
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]

        print("Type of order:", type(order), order)

        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','') 
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False)
    context= {'products':products,'categories':categories,'items':items,'order':order, 'user_not_login':user_not_login, 'user_login': user_login}
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

    OrderItem.objects.filter(product=None).delete()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"       
    else:
        items = []
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]

        user_not_login = "show"
        user_login = "hidden" 
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    products = Product.objects.all()
    context= {'items':items,'active_category': active_category, 'products': products, 'user_not_login':user_not_login, 'user_login': user_login, 'categories':categories}
    return render(request, 'app1/home.html',context)

def itemtrade(request):

    OrderItem.objects.filter(product=None).delete()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"   
    else:
        items = []
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]

        user_not_login = "show"
        user_login = "hidden" 
    categories = Category.objects.filter(is_sub = False)
    context= {'categories':categories,'items':items,'order':order, 'user_not_login':user_not_login, 'user_login': user_login}
    return render(request, 'app1/itemtrade.html',context)

def checkout(request):

    OrderItem.objects.filter(product=None).delete()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"   
    else:
        items = []
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]

        user_not_login = "show"
        user_login = "hidden" 
    context= {'items':items,'order':order, 'user_not_login':user_not_login, 'user_login': user_login}
    return render(request, 'app1/checkout.html',context)

def updateItem(request):

    # Xóa các OrderItem bị lỗi trước khi xử lý
    OrderItem.objects.filter(product=None).delete()  

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
 