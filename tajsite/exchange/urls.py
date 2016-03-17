from django.conf.urls import url
from . import views

app_name="exchange"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.order, name='order'),
    url(r'^order/submit/$', views.order, name='submit'),
    url(r'^orderbook/all/$', views.order_book, name='orderbookall'),
]
