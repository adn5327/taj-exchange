import sector_rec
from .models import *

def calc_taj(sec_symbol):
	cur_security = Security.objects.get(symbol=sec_symbol)

def voting_avg(cur_security):
	weight_avg = weighted_average(cur_security)
	return 10*((weight_avg - cur_security.fmv)/ cur_security.fmv)

def weighted_average(cur_security):
	bids = Order.objects.filter(order_security=cur_security,bidask='BID').order_by('-price')[:5]
	asks = Order.objects.filter(order_security=cur_security,bidask='ASK').order_by('price')[:5]
	if len(bids) <5 or len(asks) <5:
		return 0
	bid_sum = bids.aggregate(total_sum=Sum('amount'))
	ask_sum = asks.aggregate(total_sum=Sum('amount'))
	total_amount = bid_sum['total_sum'] + ask_sum['total_sum']
	avg = 0.0
	for each_bid in bids:
		avg += each_bid.price*each_bid.amount
	for each_ask in asks:
		avg += each_ask.price*each_ask.amount
	return float(avg)/ float(total_amount)

def top_orders(cur_security):
	top = Order.objects.filter(order_security=cur_security).order_by('-amount')[:3]
	if len(top) <3:
		return 0
	top_sum = top.aggregate(total_sum=Sum('amount'))
	ret = 0.0
	for each_top in top:
		weight = each_top.amount/top_sum['total_sum']
		if each_top.bidask == "BID":
			ret += weight
		else:
			ret -= weight
	return ret
	



