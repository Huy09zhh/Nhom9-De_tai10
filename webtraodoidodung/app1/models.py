from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
# Change form register django

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Số dư

    def __str__(self):
        return f"{self.user.username} - {self.balance}"

# Category
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete = models.CASCADE, related_name = 'sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return self.name
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")  # Người bán
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=200,null=True)
    price = models.PositiveIntegerField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    detail = models.TextField(null=True,blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)  # Số lượng đang bán
    sold_quantity = models.PositiveIntegerField(default=0)   # Số lượng đã bán

    def __str__(self):
        return f"{self.name} - {self.seller.username}"

    def is_out_of_stock(self):
        return self.stock_quantity <= 0  # Kiểm tra hết hàng hay chưa

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    @property
    def get_itemtrade_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_itemtrade_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class TradeAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    phonenumber = models.CharField(max_length=10,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
        
