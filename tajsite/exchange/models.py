from __future__ import unicode_literals

from django.db import models

class Security(models.Model):
	symbol = models.CharField(primary_key=True,max_length=5)
	volume = models.IntegerField(default=0)
	inner_bid = models.IntegerField(default=0)
	inner_ask = models.IntegerField(default=0)
	fmv = models.IntegerField(default=0)
	security_orders = models.ManyToManyField('Order', blank=True)
	security_accounts = models.ManyToManyField('Account', blank=True)
	#inner_bid, inner_ask, and fmv come from orders db

	def __str__(self):
		return self.symbol

class Order(models.Model):
	start_time = models.DateTimeField('date started')
	order_type = models.CharField(max_length=20,choices=(('Fill or Kill','Fill or Kill'),))
	bidask = models.CharField(max_length=3,choices=(('BID', 'BID'),('ASK', 'ASK')))
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	order_security = models.ForeignKey('Security', on_delete=models.CASCADE)
	order_account = models.ForeignKey('Account', on_delete=models.CASCADE)
	#NEED  'TRADE' RELATIONSHIP WITH ORDER
	#need to update order_type, order_id

	def __str__(self):
		return str(self.order_id)+': '+self.bidask+' on ' + self.order_security.symbol+' - '+str(self.amount)+' at '+str(self.price)
		
class Account(models.Model):
	name = models.CharField(max_length=20)
	funds = models.IntegerField(default=0)
	SSN = models.IntegerField(primary_key=True,default=0)
	account_num = models.IntegerField(default=0)
	account_securities = models.ManyToManyField('Security', blank=True)
	account_orders = models.ManyToManyField('Order', blank=True)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (("SSN", "account_num"),)			