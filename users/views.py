from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse('Hello, World!')

def login(request):
    return render (request, 'login.html')