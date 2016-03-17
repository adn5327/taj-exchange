from django.shortcuts import render
from django.http import HttpResponse

from django.utils import timezone

from .forms import OrderForm
from .models import Order, Security, Account

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
		bids = Order.objects.filter(order_security=sec,bidask='BID')
		asks = Order.objects.filter(order_security=sec,bidask='ASK')
		book[sec.symbol] = {'bids':bids,'asks':asks}
	context={
		'book':book
	}
	return render(request, 'exchange/orderbook.html',context)




