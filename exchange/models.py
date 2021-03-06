from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone


class Security(models.Model):
	symbol = models.CharField(primary_key=True,max_length=5)
	sector = models.CharField(default='Unknown',max_length=25)
	name = models.CharField(default='NameGoesHere',max_length=25)
	volume = models.IntegerField(default=0)
	inner_bid = models.FloatField(default=0)
	inner_ask = models.FloatField(default=0)
	fmv = models.FloatField(default=0)
	
	def updateFMV(self, new_fmv):
		self.fmv = new_fmv
		self.save()

	def __str__(self):
		return self.symbol

class Possessions(models.Model):
	account_id = models.ForeignKey('Account', related_name="pos_account_id", on_delete=models.CASCADE)
	security_id = models.ForeignKey('Security', related_name="pos_security_id", on_delete=models.CASCADE)
	available_amount = models.IntegerField(default=0)
	total_amount = models.IntegerField(default=0)
	class Meta:
		unique_together = (('account_id', 'security_id'))

	def updateTotal(self, amount_change):
		self.total_amount += amount_change
		self.save()

	def updateAvailable(self, amount_change):
		self.available_amount += amount_change
		self.save()

	def updateBoth(self, amount_change):
		self.total_amount += amount_change
		self.available_amount += amount_change
		self.save()

	def __str__(self):
		return self.security_id.symbol + ': Available shares = ' \
			+ str(self.available_amount) + ' Total shares = ' \
			+ str(self.total_amount) + ' shares'

	def print_shares_avail(self):
		return 'Available Shares: ' + str(self.available_amount) + ' shares'
	
	def print_shares_tot(self):
		return 'Total Shares: ' + str(self.total_amount) + ' shares'


class Trade(models.Model):
	trade_id = models.AutoField(primary_key=True)
	bid_account = models.ForeignKey('Account', related_name="bid_account", on_delete=models.DO_NOTHING)
	ask_account = models.ForeignKey('Account', related_name="ask_account", on_delete=models.DO_NOTHING)
	security_id = models.ForeignKey('Security', related_name="trade_security_id", on_delete=models.DO_NOTHING)
	price = models.FloatField(default=0)
	amount = models.IntegerField(default=0)
	date_time = models.DateTimeField()


	def __str__(self):
		return str(self.trade_id) + ': ' + str(self.security_id) + ', ' + str(self.price) + ', ' + str(self.amount)	

class Order(models.Model):
	start_time = models.DateTimeField('date started')
	order_type = models.CharField(max_length=20,choices=(('Limit','Limit'),))
	bidask = models.CharField(max_length=3,choices=(('BID', 'BID'),('ASK', 'ASK')))
	price = models.FloatField(default=0)
	amount = models.IntegerField(default=0)
	order_security = models.ForeignKey('Security', on_delete=models.CASCADE)
	order_account = models.ForeignKey('Account', on_delete=models.CASCADE)

	def update(self, amount_change):
		if self.amount >= amount_change:
			self.amount -= amount_change
			self.save()
			return True
		else:
			return False


	def __str__(self):
		return str(self.id)+': '+self.bidask+' on ' + str(self.order_security) +' : '+str(self.amount)+' at $'+str(self.price)

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	total_funds = models.FloatField(default=0)
	available_funds = models.FloatField(default=0)
	SSN = models.IntegerField(default=0)

	def updateTotal(self, change_in_funds):
		self.total_funds += change_in_funds
		self.save()
	
	def updateAvailable(self, change_in_funds):
		self.available_funds += change_in_funds
		self.save()

	def updateBoth(self, changeTotal, changeAvailable):
		self.total_funds += changeTotal
		self.available_funds += changeAvailable
		self.save()

	def __str__(self):
		return self.user.username
	def print_funds_avail(self):
		return 'Available Funds: ' + str(self.available_funds)
	def print_funds_tot(self):
		return 'Total Funds: ' + str(self.total_funds)
	class Meta:
		unique_together = (("SSN", "id"))
