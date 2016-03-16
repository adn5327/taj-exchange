from django.contrib import admin

from .models import Security, Order, Account

admin.site.register(Security)
admin.site.register(Order)
admin.site.register(Account)
