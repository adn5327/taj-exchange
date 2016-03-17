from django.shortcuts import render
from django.http import HttpResponse

from django.utils import timezone

from .forms import OrderForm
from .models import Order

def index(request):
    return HttpResponse("Hello. Welcome to the Taj Exchange")

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
		return render(request, "order_submit.html", context)
	else:
		form = OrderForm()
		context = {
			'form':form
		}
		return render(request, 'order.html', context)


