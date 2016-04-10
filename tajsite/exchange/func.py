from .forms import OrderForm, CreateAccountForm, UpdateAccountForm

from .models import Order, Security, Account

def setInners(security):
	ask_orders = Order.objects.filter(order_security=security,bidask='ASK').order_by('price')
	bid_orders = Order.objects.filter(order_security=security,bidask='BID').order_by('-price')
	if len(ask_orders) == 0:
		security.inner_ask = 0
	else:
		security.inner_ask = ask_orders[0].price
	if len(bid_orders) == 0:
		security.inner_bid = 0
	else:
		security.inner_bid = bid_orders[0].price
	security.save()