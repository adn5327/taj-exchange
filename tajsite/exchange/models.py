from __future__ import unicode_literals

from django.db import models

class Security(models.Model):
	symbol = models.CharField(max_length=5)
	volume = models.IntegerField(default=0)
	inner_bid = models.IntegerField(default=0)
	inner_ask = models.IntegerField(default=0)
	fmv = models.IntegerField(default=0)
	#inner_bid, inner_ask, and fmv come from orders db
	#NEED  'HAS' RELATIONSHIP WITH ACCOUNT
	#NEED  'HAS' RELATIONSHIP WITH ORDER



	def __str__(self):
		return self.symbol

class Order(models.Model):
	start_time = models.DateTimeField('date started')
	order_type = models.CharField(max_length=20)
	bid = models.BooleanField(default=True)
	ask = models.BooleanField(default=False)
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	order_id = models.IntegerField(default=0)
	security = #relationship
	#NEED  'HAS' RELATIONSHIP WITH SECURITY
	#NEED  'TRADE' RELATIONSHIP WITH ORDER
	#NEED  'PLACES' RELATIONSHIP WITH ACCOUNT
	#need to update order_type, order_id

	def __str__(self):
		if(self.bid)
			return str(self.order_id)+': BID on ' + self.security+' - +str(self.amount)+' at '+str(self.price) 
class Account(models.Model):
	name = models.CharField(max_length=20)
	funds = models.IntegerField(default=0)
	SSN = models.IntegerField(default=0)
	account_num = models.IntegerField(default=0)
	#NEED  'PLACES' RELATIONSHIP WITH ORDER
	#NEED  'HAS' RELATIONSHIP WITH SECURITY

	def __str__(self):
		return self.name			