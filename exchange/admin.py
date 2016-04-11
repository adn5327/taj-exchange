from django.contrib import admin

from .models import Security, Order, Account

from django.contrib.auth.models import User, Permission, Group


admin.site.register(Security)
admin.site.register(Order)
admin.site.register(Account)

