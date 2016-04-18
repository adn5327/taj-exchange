from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import timezone
from django.core.urlresolvers import reverse

from .forms import OrderForm, CreateAccountForm, UpdateAccountForm, LoginAccountForm

from .models import Order, Security, Account, Possessions,Trade

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .func import orderSubmission, setInners, closeAndRender, closeAndRedirect, placeOrder
from . import sector_rec, tajindicator

def index(request):

	return closeAndRedirect('exchange:orderbookall')


def order(request):
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data
			f_bidask = f['bidask']
			f_price = f['price']
			f_amount = f['amount']
			f_user = request.user
			f_order_security = f['order_security']
			context = placeOrder(f_bidask, f_price, f_amount, f_user, f_order_security)
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
    if request.method == 'POST':
        sectorpost = request.POST['sector']
        if sectorpost == 'all':
            securities = Security.objects.all()
        elif sectorpost == 'yours':
            account = Account.objects.get(user=request.user)
            pos = Possessions.objects.filter(account_id=account)
            secs = []
            for p in pos:
                secs.append(p.security_id.symbol)
            securities = Security.objects.filter(symbol__in=secs) 
        else:
            securities = Security.objects.filter(sector=sectorpost)
    else: 
	    securities = Security.objects.all().order_by('-fmv')[:10]
    for sec in securities:
		bids = Order.objects.filter(order_security=sec,bidask='BID').order_by('-price')
		asks = Order.objects.filter(order_security=sec,bidask='ASK').order_by('price')
		book[sec.symbol] = {'bids':bids,'asks':asks, 'sector':sec.sector, 'fmv':sec.fmv}
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
			
			if order.bidask == 'BID':
				account = Account.objects.get(user=request.user)
				account.updateAvailable(order.price*order.amount)
			else:
				pos = Possessions.objects.filter(account_id=order.order_account, security_id=order.order_security)[0]
				pos.updateAvailable(order.amount)

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

def taj_it(request):
	if request.method== 'POST':
		security = Security.objects.get(symbol=request.symbol)
		taj_indicator = tajindicator.calc_taj(security)	
		if abs(taj_indicator) > request.taj_value:
			if taj_indicator <0:
				bidask='ASK'
			else:
				bidask='BID'
			placeOrder(bidask,security.fmv, request.amount, request.user, security) 
		return closeAndRedirect('exchange:viewaccount')

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

	risk, total_shares = sector_rec.calculate_current_risk(account)
	agr_low, agr_high = sector_rec.aggressive(risk, total_shares)
	mod_low, mod_high = sector_rec.moderate(risk, total_shares)
	safe_low, safe_high = sector_rec.safe(risk, total_shares)
	context = {
		'account':account,
		'orders':orders,
		'possessions':possessions,
		'user':request.user,
		'risk':risk,
		'agr_low':agr_low,
		'agr_high':agr_high,
		'mod_low':mod_low,
		'mod_high':mod_high,
		'safe_low':safe_low,
		'safe_high':safe_high,
	}

	return closeAndRender(request, 'exchange/view_account.html',context) 

def view_security(request, symbol):
	security = Security.objects.get(symbol=symbol)
	trades = Trade.objects.filter(security_id=security).order_by('-date_time')[:10]
	bids = Order.objects.filter(order_security=security,bidask='BID').order_by('-price')
	asks = Order.objects.filter(order_security=security,bidask='ASK').order_by('price')	
	taj_indicator = tajindicator.calc_taj(security)	
	if request.user.is_authenticated():
		account = Account.objects.get(user=request.user)
		possessions = Possessions.objects.filter(account_id=account, security_id=security)
		bidform = OrderForm(initial={'bidask':"BID",'order_security':security})
		askform = OrderForm(initial={'bidask':"ASK",'order_security':security})
		context = {
			'security':security,
			'trades':trades,
			'account':account,
			'bids':bids,
			'asks':asks,
			'possessions':possessions,
			'user':request.user,
			'bidform':bidform,
			'askform':askform,
			'tajindicator':taj_indicator,
		}
	else:
		context = {
			'security':security,
			'trades':trades,
			'bids':bids,
			'asks':asks,
			'user':request.user,
		}

	return closeAndRender(request, 'exchange/view_security.html', context)
