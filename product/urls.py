"""np URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import product
from . import views


urlpatterns = [
	path('', views.index, name='home'),
	path('allproducts/', views.allproducts, name='allproducts'),
	path('orders/', views.orders, name='orders'),
	path('viewItem/<int:id>', views.viewItem, name='viewItem'),
	path('cancelItem/<int:id>', views.cancelItem, name='cancelItem'),
	path('categories/', views.categories, name='categories'),
	path('users/', views.users, name='users'),
	path('addProduct/', views.addProduct, name='addProduct'),
	path('edit/<int:id>', views.editProduct, name='editProduct'),
	path('editProduct/', views.editProductData, name='editProductData'),
	path('delete/<int:id>', views.deleteProduct, name='deleteProduct'),
	path('editCategory/<int:id>', views.editCategory, name='editCategory'),
	path('editCat/', views.editCat, name='editCategory'),
	path('deleteCategory/<int:id>', views.deleteCategory, name='deleteCategory'),
	path('addCategory/', views.addCategory, name='addCategory'),
]
