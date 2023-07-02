from django.contrib import admin

# Register your models here.
from .models import Dish, MenuSection, Order, Staff, Store

# Register your models here.
admin.site.register(Dish)
admin.site.register(MenuSection)
admin.site.register(Order)
admin.site.register(Staff)
admin.site.register(Store)
