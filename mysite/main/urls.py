from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("home/",views.home,name="home"),
    path("index/",views.index,name="index"),
    path("institutions/",views.institution,name='institutions'),
    path("courses/",views.course,name="courses"),
    path("clusters/",views.cluster,name="clusters")
]