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
    courses = Course.objects.filter(certification__isnull=False).distinct()
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

     # Prepare course information to pass to the template
    course_data = {
        'programme_name': course.programme_name,
        'cluster': course.cluster,
        'cluster_subjects': [course.cluster_subject_1, course.cluster_subject_2, course.cluster_subject_3, course.cluster_subject_4],
        'minimum_subjects': [
            {'subject': course.minimum_subject_1, 'grade': course.minimum_subject_1_grade},
            {'subject': course.minimum_subject_2, 'grade': course.minimum_subject_2_grade},
            {'subject': course.minimum_subject_3, 'grade': course.minimum_subject_3_grade},
            {'subject': course.minimum_subject_4, 'grade': course.minimum_subject_4_grade},
        ],
        'minimum_mean_grade': course.minimum_mean_grade,
    }
        # Prepare certifications data to pass to the template

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

    return render(response, 'main/certifications_by_programme.html', {'certifications_data': certifications_data, 'course_data': course_data})


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

    
    

def courses_by_cluster(response,cluster):
    courses = Course.objects.filter(cluster=cluster,certification__isnull=False).distinct()
    
    return render(response, 'main/courses_by_cluster.html', {'courses':courses})
    