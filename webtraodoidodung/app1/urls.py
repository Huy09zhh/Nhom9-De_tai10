from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('product_create/', views.product_create,name="product_create"),
    path('product_list/', views.product_list,name="product_list"),
    path('product_update/', views.product_update,name="product_update"),
    path('detail/', views.detail,name="detail"),
    path('category/', views.category,name="category"),
    path('register/', views.register,name="register"),
    path('login/', views.loginPage,name="login"),
    path('logout/', views.logoutPage,name="logout"),
    path('search/', views.search,name="search"),
    path('itemtrade/', views.itemtrade,name="itemtrade"),
    path('checkout/', views.checkout,name="checkout"),
    path('update_item/', views.updateItem,name="update_item"),  

]
