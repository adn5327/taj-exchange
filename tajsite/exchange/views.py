from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import timezone
from django.core.urlresolvers import reverse

from .forms import OrderForm, CreateAccountForm, UpdateAccountForm

from .models import Order, Security, Account

from .func import setInners

def index(request):
    return render(request, 'exchange/index.html' )

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
			a = Account(name=f['name'],
				SSN = f['SSN'])
			a.save()
			context = {
				'account':a
			}
		else:
			context = {
				'account':None
			}
		return render(request, 'exchange/create_account_submit.html', context)
	else:
		form = CreateAccountForm()
		context = {
			'form':form
		}
		return render(request, 'exchange/create_account.html', context)
		

def update_account(request):
   if request.method== 'POST':
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

