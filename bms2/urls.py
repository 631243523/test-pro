"""bms2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('get_valid_img/', views.get_valid_img),
    path('logout/', views.logout),
    path('register/', views.register),
    path('setpwd/', views.setpwd),
    path('', views.login),
    path('select/', views.select),
    path('setup/', views.setup),
    path('give/', views.give),
    path('page/', views.page),
    path('index/', views.index),
    path('index2/', views.index2,name='index2'),
    path('index3/', views.index3),
    path('add/', views.add),
    path('add2/', views.add2),
    path('add3/', views.add3),
    re_path('update/(\d+)', views.update),
    re_path('update2/(\d+)', views.update2),
    re_path('update3/(\d+)', views.update3),
    re_path('delete/(\d+)', views.delete),
    re_path('delete2/(\d+)', views.delete2),
    re_path('delete3/(\d+)', views.delete3),
]
