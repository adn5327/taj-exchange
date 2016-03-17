from django import forms
from datetime import datetime

class Order(forms.Form):
	#start_time = models.DateTimeField('date started')
	order_type = forms.CharField(max_length=20,choices=(('Fill or Kill','Fill or Kill'),))
	bidask = forms.CharField(max_length=3,choices=(('BID', 'BID'),('ASK', 'ASK')))
	price = forms.IntegerField(initial=0)
	amount = forms.IntegerField(initial=0)
	order_id = forms.IntegerField(primary_key=True,initial=0)
	order_security = forms.ForeignKey('Security', on_delete=models.CASCADE)
	order_account = forms.ForeignKey('Account', on_delete=models.CASCADE)