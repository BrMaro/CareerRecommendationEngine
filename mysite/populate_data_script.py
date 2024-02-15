import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from main.models import Certification
from institutions.models import Institution
from course.models import Course

def populate_data():
    institutions_from_existing_db = Institution.objects.using("CampusCourses").all()

    for institution_data in institutions_from_existing_db:
        Institution.objects.create(
            id=institution_data.id,
            alias=institution_data.alias,
            Iname=institution_data.Iname,
            Category=institution_data.Category,
            institution_type=institution_data.institution_type,
            Parent_Ministry=institution_data.Parent_Ministry
        )

    course_from_existing_db = Course.objects.using("CampusCourses").all()
    for course_data in course_from_existing_db:
        Course.objects.create(
            course_id=course_data.course_id,
            programme_name=course_data.programme_name,
            Cluster=course_data.Cluster,
            Cluster_subject_1=course_data.Cluster_subject_1,
            Cluster_subject_2=course_data.Cluster_subject_2,
            Cluster_subject_3=course_data.Cluster_subject_3,
            Cluster_subject_4=course_data.Cluster_subject_4,
            Minimum_subject_1=course_data.Minimum_subject_1,
            Minimum_subject_1_grade=course_data.Minimum_subject_1_grade,
            Minimum_subject_2=course_data.Minimum_subject_2,
            Minimum_subject_2_grade=course_data.Minimum_subject_2_grade,
            Minimum_subject_3=course_data.Minimum_subject_3,
            Minimum_subject_3_grade=course_data.Minimum_subject_3_grade,
            Minimum_subject_4=course_data.Minimum_subject_4,
            Minimum_subject_4_grade=course_data.Minimum_subject_4_grade,
            Minimum_Mean_Grade=course_data.Minimum_Mean_Grade,
        )

    certifications_from_existing_db = Certification.objects.using('CampusCourses').all()

    for certification_data in certifications_from_existing_db:
        Certification.objects.create(
            Programme_Code=certification_data.Programme_Code,
            Iname=certification_data.Iname,
            Programme_name=certification_data.Programme_name,
            Programme_Name_in_campus=certification_data.Programme_Name_in_campus,
            Year_1_Programme_cost=certification_data.Year_1_Programme_cost,
            _2022_cut_off=certification_data._2022_cut_off,
            _2021_cut_off=certification_data._2021_cut_off,
            _2020_cut_off=certification_data._2020_cut_off,
        )


populate_data()
