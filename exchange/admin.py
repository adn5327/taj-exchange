from django.contrib import admin

from .models import Security, Order, Account, Possessions, Trade

from django.contrib.auth.models import User, Permission, Group


admin.site.register(Security)
admin.site.register(Order)
admin.site.register(Account)
admin.site.register(Possessions)
admin.site.register(Trade)


