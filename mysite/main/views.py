from django.shortcuts import render
from django.http import HttpResponse, request

# Create your views here.

def index(response):
    return HttpResponse("Hello, World!")

def home(response):
    return render(request, "main/base.html")