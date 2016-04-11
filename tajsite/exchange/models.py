from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

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

class Posessions(models.Model):
	account = models.ForeignKey('Account', on_delete=models.CASCADE)
	security = models.ForeignKey('Security', on_delete=models.CASCADE)
	amount = models.IntegerField(default=0)


class Trade(models.Model):
	trade_id = models.AutoField(primary_key=True)
	bid_account = models.ForeignKey('Account', related_name="bid_account", on_delete=models.DO_NOTHING)
	ask_account = models.ForeignKey('Account', related_name="ask_account", on_delete=models.DO_NOTHING)
	security = models.ForeignKey('Security', on_delete=models.DO_NOTHING)
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)

	def __str__(self):
		return str(self.trade_id) + ': ' + str(self.security) + ', ' + str(self.price) + ', ' + str(self.amount)	

class Order(models.Model):
	start_time = models.DateTimeField('date started')
	order_type = models.CharField(max_length=20,choices=(('Limit','Limit'),))
	bidask = models.CharField(max_length=3,choices=(('BID', 'BID'),('ASK', 'ASK')))
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	order_security = models.ForeignKey('Security', on_delete=models.CASCADE)
	order_account = models.ForeignKey('Account', on_delete=models.CASCADE)
	#NEED  'TRADE' RELATIONSHIP WITH ORDER
	#need to update order_type,

	def update(self, amount_change):
		if self.amount >= amount_change:
			self.amount -= amount_change
			self.save()
			return True
		else:
			return False


	def __str__(self):
		return str(self.id)+': '+self.bidask+' on ' + str(self.order_security) +' : '+str(self.amount)+' at '+str(self.price)

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	total_funds = models.IntegerField(default=0)
	available_funds = models.IntegerField(default=0)
	SSN = models.IntegerField(default=0)
	account_securities = models.ManyToManyField('Security', blank=True)
	account_orders = models.ManyToManyField('Order', blank=True)

	def __str__(self):
		return self.user.username
	def print_funds_avail(self):
		return 'Available Funds: ' + str(self.available_funds)
	def print_funds_tot(self):
		return 'Total Funds: ' + str(self.total_funds)
	class Meta:
		unique_together = (("SSN", "id"))
