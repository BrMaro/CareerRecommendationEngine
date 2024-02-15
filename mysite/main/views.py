from django.shortcuts import render
from django.http import HttpResponse
from .models import Institution,Certification,Course

# Create your views here.

def index(response):
    return HttpResponse("Hello, World!")

def home(response):
    return render(response, "main/home.html",{})

def recommendations(response):
    return render(response, "main/home.html",{})

def course(response):
    return render(response, "main/course.html",{}) 

def institution(response):
    data = Institution.objects.all()
    return render(response, "main/institution.html",{"data":data})