from __future__ import unicode_literals

from django.db import models

class Security(models.Model):
	symbol = models.CharField(primary_key=True,max_length=5)
	volume = models.IntegerField(default=0)
	inner_bid = models.IntegerField(default=0)
	inner_ask = models.IntegerField(default=0)
	fmv = models.IntegerField(default=0)
	security_orders = models.ManyToManyField('Order')
	security_accounts = models.ManyToManyField('Account')
	#inner_bid, inner_ask, and fmv come from orders db

	def __str__(self):
		return self.symbol

class Order(models.Model):
	start_time = models.DateTimeField('date started')
	order_type = models.CharField(max_length=20)
	bid = models.BooleanField(default=True)
	ask = models.BooleanField(default=False)
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	order_id = models.IntegerField(primary_key=True,default=0)
	order_security = models.ForeignKey('Security', on_delete=models.CASCADE)
	order_account = models.ForeignKey('Account', on_delete=models.CASCADE)
	#NEED  'TRADE' RELATIONSHIP WITH ORDER
	#need to update order_type, order_id

	def __str__(self):
		if(self.bid):
			return str(self.order_id)+': BID on ' + self.security+' - '+str(self.amount)+' at '+str(self.price)
		else:
			return str(self.order_id)+': ASK on ' + self.security+' - '+str(self.amount)+' at '+str(self.price)
class Account(models.Model):
	name = models.CharField(max_length=20)
	funds = models.IntegerField(default=0)
	SSN = models.IntegerField(primary_key=True,unique=False,default=0)
	account_num = models.IntegerField(primary_key=True,unique=False,default=0)
	account_securities = models.ManyToManyField('Security')
	account_orders = models.ManyToManyField('Order')

	def __str__(self):
		return self.name			