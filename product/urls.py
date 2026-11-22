from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='all'),
    path('drinks/', views.drinks, name='drinks'),
    path('FastFood/', views.FastFood, name='FastFood'),
    path('MainCourses/', views.MainCourses, name='MainCourses'),
    path('soups/', views.soups, name='soups'),
    path('salad/', views.salad, name='salad'),
    path('pastries/', views.pastries, name='pastries'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    ]