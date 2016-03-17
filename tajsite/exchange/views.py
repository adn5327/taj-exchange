from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello. Welcome to the Taj Exchange")

def order(request):
	return render(request, 'order.html', {})
