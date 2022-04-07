from django.contrib import admin

from .models import Orders, Product, Users, category

# Register your models here.
admin.site.register(Product)
admin.site.register(category)
admin.site.register(Users)
admin.site.register(Orders)