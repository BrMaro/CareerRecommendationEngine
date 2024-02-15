from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("home/",views.home,name="home"),
    path("index/",views.index,name="index"),
    path("institution/",views.institution,name='institution'),
    path("course/",views.course,name="course")
]