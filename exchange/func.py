from .forms import OrderForm, CreateAccountForm, UpdateAccountForm
from django.core.urlresolvers import reverse
from .models import Order, Security, Account, Trade, Possessions
from django.shortcuts import render
from django.db import connection

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



def performTrade(ask, bid, aggressor):
	if aggressor == 'ASK':
		trade_price = ask.price
	else:
		trade_price = bid.price
	print
	print ask
	print bid
	trade_amount = min(ask.amount, bid.amount)
	print trade_amount
	print type(trade_amount)
	trade = Trade(
		bid_account = bid.order_account,
		ask_account = ask.order_account,
		security = ask.order_security,
		price = trade_price,
		amount = trade_amount
		)
	print trade
	# ask.amount -= trade_amount
	# bid.amount -= trade_amount
	ask.update(trade_amount)
	bid.update(trade_amount)

	bidder_pos = Possessions.objects.filter(account=bid.account,security=bid.order_security)
	ask_pos = Possessions.objects.filter(account=ask.account,security=ask.order_security)
	if bidder_pos is None:
		bidder_pos = Possessions(
			account = bid.order_account,
			security = bid.order_security,
			amount = trade_amount)
		bidder_pos.save()
	else:
		bidder_pos.update(trade_amount)	
	if ask_pos is None:
		ask_pos = Possessions(
			account = ask.order_account,
			security = ask.order_security,
			amount = -trade_amount)
		ask_pos.save()

	else:
		ask_pos.update(-trade_amount)

	# bidder_pos.amount += trade_amount
	# ask_pos.amount -= trade_amount
	
	total_price = trade_amount * trade_price
	bid.account.updateTotal(-total_price)
	ask.account.updateTotal(total_price)

	# bid.account.total_funds -= (trade_amount * trade_price)

	# ask.account.total_funds += (trade_amount * trade_price)
	# ask.account.available_funds += (trade_amount * trade_price)

	trade.save()

def orderSubmission(order):
	if order.bidask=='ASK':
		orders = Order.objects.filter(order_security=order.order_security,bidask='BID').order_by('-price')	
	else:
		orders = Order.objects.filter(order_security=order.order_security, bidask='ASK').order_by('price')
	print orders
	print order
	if len(orders) == 0:
		return False
	continue_trading = True
	order_idx = 0
	while continue_trading:
		curr_order = orders[order_idx]
		if order.bidask == 'ASK':
			if order.price <= curr_order.price:
				print 'ASKING'
				performTrade(order, curr_order, 'ASK')
				if order.amount == 0:
					order.delete()
					continue_trading = False
				if curr_order.amount == 0:
					curr_order.delete()
				order_idx += 1
			else:
				continue_trading = False
		else:
			if order.price >= curr_order.price:
				print 'BIDDING'
				performTrade(curr_order, order, 'BID')
				if order.amount == 0:
					order.delete()
					continue_trading = False
				if curr_order.amount == 0:
					curr_order.delete()
				order_idx += 1
			else:
				continue_trading = False
def closeAndRedirect(url):
	print len(connection.queries)
	connection.close()
	# if rev:		
	url = reverse(url)
	return HttpResponseRedirect(url)

def closeAndRender(request, url, context):
	print len(connection.queries)
	connection.close()
	return render(request, url, context)

