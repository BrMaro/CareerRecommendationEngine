from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse("Hello, World!")

def home(response):
    return render(response, "main/home.html",{})

def clusters(response):
    return render(response, "main/clusters.html",{})

def courses(response):
    return render(response, "main/courses.html",{})

def recommendations(response):
    return render(response, "main/home.html",{})

