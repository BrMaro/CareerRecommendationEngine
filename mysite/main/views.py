from django.shortcuts import render
from django.http import HttpResponse
from .models import Institution,Certification,Course
from django.shortcuts import get_object_or_404

# Create your views here.

def index(response):
    return HttpResponse("Hello, World!")


def home(response):
    return render(response, "main/home.html",{})


def recommendations(response):
    return render(response, "main/home.html",{})


def course(response):
    courses = Course.objects.all()
    return render(response, "main/courses.html",{"courses":courses}) 


def cluster(response):
    clusters = Course.objects.values_list('cluster', flat=True).distinct()
    return render(response, "main/clusters.html",{'clusters':clusters})


def institution(response):
    data = Institution.objects.all()
    return render(response, "main/institutions.html",{"data":data})


def certifications_by_programme(response,programme_name):
    course = get_object_or_404(Course, programme_name=programme_name)
    print(course)
    certifications = Certification.objects.filter(programme_name=course)
    print(certifications[0])
    certifications_data = []
    for certification in certifications:
        institution = certification.iname   #extract related Institution object     
        
        certification_data = {
            'programme_code': certification.programme_code,
            'category': institution.category,
            'iname': institution.iname,
            'year_1_programme_cost':certification.year_1_programme_cost
        }
        certifications_data.append(certification_data)
    return render(response, 'main/certifications_by_programme.html', {'certifications_data': certifications_data, 'programme_name': programme_name})


def courses_by_institution():
    pass

def courses_by_cluster():
    pass