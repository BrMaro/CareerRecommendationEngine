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

def cluster(response):
    clusters = Course.objects.values_list('cluster', flat=True).distinct()
    return render(response, "main/clusters.html",{'clusters':clusters})


def institution(response):
    data = Institution.objects.all()
    return render(response, "main/institution.html",{"data":data})