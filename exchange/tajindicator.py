import sector_rec
from django.db.models import Sum
from .models import *

def calc_taj(cur_security):
	if cur_security.fmv == 0:
		return 0
	avg = voting_avg(cur_security)
	big_fish = top_orders(cur_security)
	combined = .66*avg + .34*big_fish
	sector_multiplier = 1/(sector_rec.risk_map[cur_security.sector] + .5)
	ret_val = sector_multiplier * combined
	if ret_val >1:
		return 1
	if ret_val < -1:
		return -1
	return ret_val

def voting_avg(cur_security):
	if cur_security.fmv == 0:
		return 0
	weight_avg = weighted_average(cur_security)
	if weight_avg == 0:
		return 0
	return 10*((weight_avg - cur_security.fmv)/ cur_security.fmv)

def weighted_average(cur_security):
	if cur_security.fmv == 0:
		return 0
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
		weight = (1.0*each_top.amount)/top_sum['total_sum']
		if each_top.bidask == "BID":
			ret += weight
		else:
			ret -= weight
	return ret
	



