from django.shortcuts import render
from django.http import HttpResponse

from .forms import OrderForm
from .models import Order

def index(request):
    return HttpResponse("Hello. Welcome to the Taj Exchange")

def order(request):
	form = OrderForm()
	context = {
		'form':form
	}
	return render(request, 'order.html', context)

def order_submit(request):
	form = OrderForm(request.POST)
	if form.is_valid():
		f = form.cleaned_data
		o = Order(order_type=f['order_type'],bidask=f['bidask'],price=f['price'],amount=f['amount'])
		o.save()
		context = {
			'order':o,
		}
	else:
		context = {
			'order':None
		}
	return render(request, "order_submit.html", context)

