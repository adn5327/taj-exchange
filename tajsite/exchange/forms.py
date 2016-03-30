from django import forms
from datetime import datetime

from .models import Security,Order,Account

class OrderForm(forms.Form):
	#start_time = models.DateTimeField('date started')
	order_type = forms.ChoiceField(choices=(('Fill or Kill','Fill or Kill'),))
	bidask = forms.ChoiceField(choices=(('BID', 'BID'),('ASK', 'ASK')))
	price = forms.IntegerField(initial=0)
	amount = forms.IntegerField(initial=0)
	order_security = forms.ModelMultipleChoiceField(queryset=Security.objects.all())
	#order_account = forms.ModelMultipleChoiceField(queryset=Account.objects.all())



class CreateAccountForm(forms.Form):
	username = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	SSN = forms.IntegerField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())
	password_confirm = forms.CharField(required=True, widget=forms.PasswordInput())

class LoginAccountForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())


class UpdateAccountForm(forms.Form):
    #order_account = forms.ModelMultipleChoiceField(queryset=Account.objects.all())
    funds = forms.IntegerField(initial=0)

