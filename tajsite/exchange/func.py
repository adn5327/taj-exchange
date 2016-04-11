from .forms import OrderForm, CreateAccountForm, UpdateAccountForm

from .models import Order, Security, Account, Trade, Posessions

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

	trade_amount = min(ask.amount, bid.amount)

	trade = Trade(
		bid_account = bid.id,
		ask_account = ask.id,
		security = ask.security,
		price = trade_price,
		amount = trade_amount
		)

	ask.amount -= trade_amount
	bid.amount -= trade_amount

	bidder_pos = Posession.objects.filter(account=bid.account,security=bid.security)
	ask_pos = Posession.objects.filter(account=ask.account,security=ask.security)

	bidder_pos.amount += trade_amount
	ask_pos.amount -= trade_amount
	
	bid.account.total_funds -= (trade_amount * trade_price)

	ask.account.total_funds += (trade_amount * trade_price)
	ask.account.available_funds += (trade_amount * trade_price)

	trade.save()

def orderSubmission(order):
	if order.bidask=='ASK':
		orders = Order.objects.filter(order_security=order.security,bidask='BID').order_by('-price')	
	else:
		orders = Order.objects.filter(order_security=order.security, bidask='ASK').order_by('price')

	if len(orders) == 0:
		return False
	continue_trading = True
	order_idx = 0
	while continue_trading:
		curr_order = orders[order_idx]
		if order.bidask == 'ASK':
			if order.price <= curr_order.price:
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
				performTrade(order, curr_order, 'BID')
				if order.amount == 0:
					order.delete()
					continue_trading = False
				if curr_order.amount == 0:
					curr_order.delete()
				order_idx += 1
			else:
				continue_trading = False



