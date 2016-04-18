from django.conf.urls import url
from . import views

app_name="exchange"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.order, name='order'),
    url(r'^order/submit/$', views.order, name='submit'),
    url(r'^orderbook/all/$', views.order_book, name='orderbookall'),
    url(r'^orderbook/(?P<symbol>[-\w]+)/$', views.view_security, name='viewsecurity'),
    url(r'^deleteorder/$', views.delete_order, name='deleteorder'),

    url(r'^account/create/', views.create_account, name='createaccount'),
    url(r'^account/create/submit', views.create_account, name='createaccountsubmit'),
    url(r'^account/login/', views.login_page, name='login'),
    url(r'^account/login/submit', views.login_page, name='loginsubmit'),
    url(r'^account/logout', views.logout_page, name='logout'),

    url(r'^account/update/$', views.update_account, name='updateaccount'),
    url(r'^account/view/$', views.view_account, name='viewaccount'),

    url(r'^account/view/t$', views.taj_it, name='tajit'),


]
