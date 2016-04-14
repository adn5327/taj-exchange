from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import timezone
from django.core.urlresolvers import reverse

from .forms import OrderForm, CreateAccountForm, UpdateAccountForm, LoginAccountForm

from .models import Order, Security, Account, Possessions

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .func import orderSubmission, setInners, closeAndRender, closeAndRedirect


def index(request):

	return closeAndRedirect('exchange:orderbookall')


def order(request):
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data
			start_time = timezone.now()
			account = Account.objects.get(user=request.user)
			o = Order(start_time=start_time,
				order_type=f['order_type'],
				bidask=f['bidask'],
				price=f['price'],
				amount=f['amount'],
				order_security=f['order_security'][0],
				order_account=account)
			error=None
			if o.bidask == 'BID':
				if o.price * o.amount <= account.available_funds:
					o.save()
					setInners(o.order_security)
					account.available_funds -= o.price*o.amount
					account.save()

					orderSubmission(o) #Performs routine to attempt trades
				else: 
					error = 'Not enough funds in your account'
					o = None
			else:#When it is an ASK

				acct_pos = Possessions.objects.filter(account_id=o.order_account,security_id=o.order_security)
				if acct_pos and acct_pos[0].amount >= o.amount:
					o.save()
					setInners(o.order_security)
					orderSubmission(o)
				else:
					error = 'You don\'t own that amount of that security'
					o = None

			context = {
				'error':error,
				'order':o,
			}
		else:
			error='Invalid form entry'
			context = {
				'error':error,
				'order':None
			}

		return closeAndRender(request, "exchange/order_submit.html", context)

	else:
		form = OrderForm()
		context = {
			'form':form,
			'user':request.user
		}
		return closeAndRender(request, 'exchange/order.html', context)


def order_book(request):
	book = {}
	securities = Security.objects.all()
	for sec in securities:
		bids = Order.objects.filter(order_security=sec,bidask='BID').order_by('-price')
		asks = Order.objects.filter(order_security=sec,bidask='ASK').order_by('price')
		book[sec.symbol] = {'bids':bids,'asks':asks}
	context={
		'book':book,
		'user':request.user
	}
	return closeAndRender(request, 'exchange/orderbook.html',context)


def delete_order(request):
	if request.method == 'POST':
		order_ids = request.POST.getlist('order')
		for order_id in order_ids:
			order = Order.objects.get(id=order_id)
			order.delete()
			setInners(order.order_security)
			account = Account.objects.get(user=request.user)
			if order.bidask == 'BID':
				account.available_funds += order.price*order.amount
				account.save()

		return closeAndRedirect('exchange:index')
	else:
		account = Account.objects.get(user=request.user)
		orders = Order.objects.filter(order_account=account)
		context={
			'orders':orders
		}
		return closeAndRender(request, 'exchange/delete_order.html',context)


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
				user = authenticate(username=f['username'],password=f['password'])
				login(request,user)
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
		return closeAndRender(request, 'exchange/create_account_submit.html', context)
	else:
		form = CreateAccountForm()
		context={
			'form':form,
			'user':request.user
		}
		return closeAndRender(request, 'exchange/create_account.html', context)

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
			else:
				form = LoginAccountForm()
				error = 'Could not log you in. Please try again'
				context={
					'form':form,
					'user':request.user,
					'error':error
				}
				return closeAndRender(request, 'exchange/login_page.html',context)
		return closeAndRedirect('exchange:index')
	else:
		form = LoginAccountForm()
		context={
			'form':form,
			'user':request.user,
			'error':None
		}
		return closeAndRender(request, 'exchange/login_page.html',context)

def logout_page(request):
	logout(request)
	return closeAndRedirect('exchange:index')

def update_account(request):
	if request.method == 'POST':
		form = UpdateAccountForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data
			cur_account = Account.objects.get(user=request.user)
			cur_funds_tot = cur_account.total_funds
			cur_funds_avail = cur_account.available_funds
			if cur_funds_avail + f['funds'] >=0:
				cur_account.total_funds = cur_funds_tot + f['funds']
				cur_account.available_funds = cur_funds_avail + f['funds']
				cur_account.save()                
		return closeAndRedirect('exchange:index')
	else:
		form = UpdateAccountForm()
		context={
			'form':form,
			'user':request.user
		}
		return closeAndRender(request, 'exchange/update_account.html',context) 


def view_account(request):

	account = Account.objects.get(user=request.user)
	orders = Order.objects.filter(order_account=account)
	possessions = Possessions.objects.filter(account_id=account)
	context = {
		'account':account,
		'orders':orders,
		'possessions':possessions,
		'user':request.user
	}
	
	return closeAndRender(request, 'exchange/view_account.html',context) 

