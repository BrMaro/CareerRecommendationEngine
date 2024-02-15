from django.contrib import admin
from .models import Certification,Institution,Course
 
# Register your models here.


admin.site.register(Course)
admin.site.register(Institution)
admin.site.register(Certification)