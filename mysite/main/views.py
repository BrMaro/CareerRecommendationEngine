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

    certifications = Certification.objects.filter(programme_name=course)

    if not certifications:
        return render(response,"main/no_certifications_error.html",{'certifications': []})

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


def certifications_per_institution(response, iname):
    institution = get_object_or_404(Institution, iname=iname)
    print(institution)
    certifications = Certification.objects.filter(iname=institution)
    
    if not certifications:
        return render(response,"main/no_certifications_error.html",{'certifications': []})

    certifications_data = []
    for certification in certifications:
        institution = certification.iname   #extract related Institution object     
        print(institution)
        course = certification.programme_name

        certification_data = {
            'programme_code': certification.programme_code,
            'category': institution.category,
            'iname': institution.iname,
            'programme_name':course.programme_name,
            'year_1_programme_cost':certification.year_1_programme_cost
        }
        certifications_data.append(certification_data)
    return render(response, 'main/certifications_per_institution.html',{'certifications_data': certifications_data, 'iname': iname})

    
    

def courses_by_cluster():
    pass