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
from . import views


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.index, name='home'), # url for main home page
	path('reg/', views.registration, name='registration'), # url for registration page
	path('register/', views.register, name='register'), # url for register after form submission
	path('log/', views.log, name='log'), # url for login page
	path('login/', views.login, name='login'), # url for login after form submission
	path('adminlogout/', views.adminlogout, name='adminlogout'), # url for admin logout
	path('userlogout/', views.userlogout, name='userlogout'), # url for user logout
	path('allcategories/', views.allCategories, name='allcategories'), # url for categories page
	path('allcategories/category/<int:id>', views.singleCategory, name='singleCategory'), # url for single category page
	path('productDetails/<int:id>', views.productDetails, name='productDetails'), # url for product detail page
	path('cart/', views.cart, name='cart'), # url for add to cart page
	path('addToCart/<int:id>', views.addToCart, name='addToCart'), # url for add to cart page
	path('addToCartAction/', views.addToCartAction, name='addToCartAction'), # url for add to cart page
	path('clearCart/', views.clearCart, name='clearCart'), # url for add to cart page
	path('undoLastEntry/', views.undoLastEntry, name='clearCart'), # url for add to cart page
	path('delcartitem/<int:id>', views.delCartItem, name='delCartItem'), # url for add to cart page
	path('buyNow/', views.buyNow, name='buyNow'), # url for add to cart page
	path('submitfinal/', views.submitFinal, name='submitFinal'), # url for add to cart page
	path('order/', views.order, name='order'), # url for add to cart page
	path('endsession/', views.endsession, name='endsession'), # url for add to cart page
	path('product/', include('product.urls')), # product urls
	path('forgotpassword/', views.forgotpassword, name='forgotpassword'), # forgotpassword
	path('verifyemail/', views.verifyEmail, name='verifyEmail'), # verify email to reset database
	path('verifyotp/', views.verify_otp, name='verifyotp'), # verify otp to reset database
	path('checkotp/', views.check_otp, name='checkotp'), # verify otp to reset database
	path('changepassword/', views.changePassword, name='changePassword'), # verify otp to reset database
	path('newpassword/', views.newPassword, name='newPassword'), # verify otp to reset database
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)