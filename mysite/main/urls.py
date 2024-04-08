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
    path('questionnaire_view/', v.questionnaire_view, name='questionnaire_view'),
    path('recommendations/',v.recommendations,name="recommendations"),
    path('certifications/<path:programme_name>/',views.certifications_by_programme,name='certifications_by_programme'),
    path('institutions/<path:iname>/',views.certifications_per_institution,name='certifications_per_institution'),
    path('clusters/<path:cluster>',views.courses_by_cluster,name='courses_by_cluster'),
    path('update_recommendations/', v.update_recommendations, name='update_recommendations'),

]