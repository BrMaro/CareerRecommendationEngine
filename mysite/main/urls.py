from django.urls import path
from . import views
from register import views as v

urlpatterns = [
    path("",views.home,name="home"),
    path("home/",views.home,name="home"),
    path("index/",views.index,name="index"),
    path("institutions/",views.institution,name='institutions'),
    path("courses/",views.course,name="courses"),
    path("clusters/",views.cluster,name="clusters"),
    path("register/",v.register,name='register'),
    path('certifications/<str:programme_name>/',views.certifications_by_programme,name='certifications_by_programme')
    
]