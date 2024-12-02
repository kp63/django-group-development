from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.

def index(request: HttpRequest):
    return render(request, 'core/welcome.html')

def handle404(request: HttpRequest):
    return render(request, '404.html')

def handle500(request: HttpRequest):
    return render(request, '500.html')
