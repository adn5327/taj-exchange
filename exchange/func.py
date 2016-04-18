from .forms import OrderForm, CreateAccountForm, UpdateAccountForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Order, Security, Account, Trade, Possessions
from django.shortcuts import render
from django.db import connection
from django.utils import timezone
from django.contrib.auth.models import User

def placeOrder(r_bidask, r_price, r_amount, r_user, r_order_security):
	start_time = timezone.now()
	account = Account.objects.get(user=r_user)
	o = Order(start_time=start_time,
		order_type="Limit",
		bidask=r_bidask,
		price=r_price,
		amount=r_amount,
		order_security=r_order_security,
		order_account=account)
	error=None
	if o.amount < 1 or o.price < 1:
		error = 'Price and amount must be greater than zero'
		o = None
	elif o.bidask == 'BID':
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
		if acct_pos and acct_pos[0].available_amount >= o.amount:
			o.save()
			setInners(o.order_security)
			acct_pos[0].updateAvailable(-o.amount)
			orderSubmission(o)
		else:
			error = 'You don\'t own that amount of that security'
			o = None

	context = {
		'error':error,
		'order':o,
	}
	return context
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

def updatePosession(account, security, trade_amount, order_type):
	if account is None or security is None or trade_amount == 0:
		return 
	pos_list = Possessions.objects.filter(account_id=account, security_id=security)
	if len(pos_list) == 0:
		pos = Possessions(
			account_id = account,
			security_id = security,
			total_amount = trade_amount,
			available_amount = trade_amount)
		pos.save()
	else:
		pos = pos_list[0]
		if pos.total_amount + trade_amount == 0:
			pos.delete()
		elif order_type == 'BID':
			pos.updateBoth(trade_amount)
		else:
			pos.updateTotal(trade_amount)


def performTrade(order, potential_order, aggressor):

	if aggressor == 'ASK':
		ask = order
		bid = potential_order
		trade_price = bid.price
	else:
		ask = potential_order
		bid = order
		trade_price = ask.price
	
	trade_amount = min(ask.amount, bid.amount)
	
	date_time = timezone.now()
	
	trade = Trade(
		bid_account = bid.order_account,
		ask_account = ask.order_account,
		security_id = ask.order_security,
		price = trade_price,
		amount = int(trade_amount),
		date_time = date_time,
		)

	ask.update(trade_amount)
	bid.update(trade_amount)
	updatePosession(bid.order_account, bid.order_security, trade_amount, 'BID') #Bid account possession increases
	updatePosession(ask.order_account, ask.order_security, -trade_amount, 'ASK') #Ask account possession decreases

	total_price = trade_amount * trade_price
	bid.order_account.updateTotal(-total_price)
	ask.order_account.updateBoth(total_price, total_price)
	bid.order_security.updateFMV(trade_price)

	trade.save()

def checkValidOrder(order, potential_order):
	if order is None or potential_order is None:
		return False
	if order.bidask == 'ASK':
		return order.price <= potential_order.price
	else:
		return order.price >= potential_order.price

def orderMatch(order, potential_order):
	if checkValidOrder(order, potential_order) == False:
		return False
	performTrade(order, potential_order, order.bidask)
	if potential_order.amount == 0:
		potential_order.delete()
	if order.amount == 0:
		order.delete()
		return False
	return True

def orderSubmission(order):
	if order.bidask=='ASK':
		orders = Order.objects.filter(order_security=order.order_security,bidask='BID').order_by('-price')	
	else:
		orders = Order.objects.filter(order_security=order.order_security, bidask='ASK').order_by('price')
	if len(orders) == 0:
		return
	continue_trading = True
	order_idx = 0
	while continue_trading:
		curr_order = orders[order_idx]
		order_idx += 1

		# Attempt to match order. If this returns false 
		# 	or if we have no more potential orders quit trading

		continue_trading = orderMatch(order, curr_order) and (order_idx < len(orders))
		# if continue_trading:
		setInners(order.order_security)

def closeAndRedirect(url):
	print len(connection.queries)
	connection.close()
	url = reverse(url)
	return HttpResponseRedirect(url)

def closeAndRender(request, url, context):
	print len(connection.queries)
	connection.close()
	return render(request, url, context)

