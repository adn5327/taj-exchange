from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import timezone
from django.core.urlresolvers import reverse

from .forms import OrderForm, CreateAccountForm, UpdateAccountForm, LoginAccountForm

from .models import Order, Security, Account

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .func import setInners

def index(request):
	if request.user.is_authenticated():
		user = request.user
	else:
		user = None
	context = {
		'user':user
	}
	return render(request, 'exchange/index.html', context)

def order(request):
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data
			start_time = timezone.now()
			o = Order(start_time=start_time,
				order_type=f['order_type'],
				bidask=f['bidask'],
				price=f['price'],
				amount=f['amount'],
				order_security=f['order_security'][0],
				order_account=f['order_account'][0])
			o.save()
			setInners(o.order_security)
			context = {
				'order':o,
			}
		else:
			context = {
				'order':None
			}
		return render(request, "exchange/order_submit.html", context)
	else:
		form = OrderForm()
		context = {
			'form':form
		}
		return render(request, 'exchange/order.html', context)


def order_book(request):
	book = {}
	securities = Security.objects.all()
	for sec in securities:
		bids = Order.objects.filter(order_security=sec,bidask='BID').order_by('-price')
		asks = Order.objects.filter(order_security=sec,bidask='ASK').order_by('price')
		book[sec.symbol] = {'bids':bids,'asks':asks}
	context={
		'book':book
	}
	return render(request, 'exchange/orderbook.html',context)


def delete_order(request):
	if request.method == 'POST':
		order_id = request.POST.get('order')
		order = Order.objects.get(id=order_id)
		order.delete()
		setInners(order.order_security)
		return redirect('/')
	else:
		orders = Order.objects.all()
		context={
			'orders':orders
		}
		return render(request, 'exchange/delete_order.html',context)


def create_account(request):
	if request.method == 'POST':
		form = CreateAccountForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data
			if f['password'] == f['password_confirm']:
				u = User.objects.create_user(username=f['username'],
					password=f['password'],
					email=f['email'])
				u.first_name = f['first_name']
				u.last_name = f['last_name']
				u.save()
				a = Account(user=u,SSN=f['SSN'])
				a.save()
				context = {
					'account':a,
					'errors':None
				}
			else:
				err = 'Passwords didn\'t match'
				context = {
					'account':None,
					'errors':err
				}
		else:
			err = 'Invalid form entry'
			context = {
				'account':None,
				'errors':err
			}
		return render(request, 'exchange/create_account_submit.html', context)
	else:
		form = CreateAccountForm()
		context = {
			'form':form
		}
		return render(request, 'exchange/create_account.html', context)

def login_page(request):
	if request.method == 'POST':
		form = LoginAccountForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data
			username = f['username']
			password = f['password']
			user = authenticate(username=username,password=password) 
			if user is not None and user.is_active:
				login(request, user)
				print "success"
		return HttpResponseRedirect(reverse('exchange:index'))
	else:
		form = LoginAccountForm()
		context={'form':form}
		return render(request, 'exchange/login_page.html',context)

def logout_page(request):
	logout(request)
	return render(request, 'exchange/logout_page.html')

def update_account(request):
	if request.method == 'POST':
		form = UpdateAccountForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data
			cur_account = Account.objects.filter(id=f['order_account'])[0]
			cur_funds = cur_account.funds
			if cur_funds + f['funds'] >=0:
				cur_account.funds = cur_funds + f['funds']
				cur_account.save()                
		return HttpResponseRedirect(reverse('exchange:index'))
	else:
		form = UpdateAccountForm()
		context={'form':form}
		return render(request, 'exchange/update_account.html',context) 


def view_account(request):
	all_accounts = Account.objects.all()
	context = {'accounts':all_accounts}
	return render(request, 'exchange/view_account.html',context) 

