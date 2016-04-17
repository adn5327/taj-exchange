import sector_rec.py
from .models import *

def calc_taj(sec_symbol):
	cur_security = Security.objects.get(symbol=sec_symbol)

def weighted_average(cur_security):
	bids = Order.objects.filter(order_security=cur_security,bidask='BID').order_by('-price')[:5]
	asks = Order.objects.filter(order_security=cur_security,bidask='ASK').order_by('price')[:5]
	bid_sum = bids.aggregate(total_sum=Sum('amount'))
	ask_sum = asks.aggregate(total_sum=Sum('amount'))
	total_amount = bid_sum['total_sum'] + ask_sum['total_sum']
	avg = 0.0
	for each_bid in bids:
		avg += each_bid.price*each_bid.amount
	for each_ask in asks:
		avg += each_ask.price*each_ask.amount
	return avg/ total_amount

def top_orders(cur_security):
	top = Order.objects.filter(order_security=cur_security).order_by('-amount')[:3]
	top_sum = top.aggregate(total_sum=Sum('amount'))
	total_pd = 0
	bids = 0
	asks = 0
	for each_top in top:
		weight = each_top.amount/top_sum
		percent_diff = (each_top.price-cur_security.fmv)/cur_security.fmv
		total_pd = total_pd + weight*percent_diff
		if each_top.bidask == "BID":
			bids += 1
		else:
			asks += 1
	



