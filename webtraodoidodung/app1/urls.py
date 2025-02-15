from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
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
