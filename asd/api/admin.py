from django.contrib import admin
from .models import Cart, Category, Product, User, MyUserManager, Order

admin.site.register(Cart)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)