from django.db import models

# Create your models here.

class Institution(models.Model):
    id = models.IntegerField(unique=True)  # Assuming 'id' is an integer field
    alias = models.CharField(max_length=255, unique=True)
    IName = models.CharField(max_length=255, primary_key=True)
    Category = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=255)
    Parent_Ministry = models.CharField(max_length=255)

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    programme_name = models.CharField(max_length=255, unique=True)
    Cluster = models.CharField(max_length=255)
    Cluster_subject_1 = models.CharField(max_length=255)
    Cluster_subject_2 = models.CharField(max_length=255)
    Cluster_subject_3 = models.CharField(max_length=255)
    Cluster_subject_4 = models.CharField(max_length=255)
    Minimum_subject_1 = models.CharField(max_length=255)
    Minimum_subject_1_grade = models.CharField(max_length=255)
    Minimum_subject_2 = models.CharField(max_length=255)
    Minimum_subject_2_grade = models.CharField(max_length=255)
    Minimum_subject_3 = models.CharField(max_length=255)
    Minimum_subject_3_grade = models.CharField(max_length=255)
    Minimum_subject_4 = models.CharField(max_length=255)
    Minimum_subject_4_grade = models.CharField(max_length=255)
    Minimum_Mean_Grade = models.CharField(max_length=255)

class Certification(models.Model):
    Programme_Code = models.IntegerField(primary_key=True)
    Iname = models.ForeignKey(Institution, on_delete=models.CASCADE)
    Programme_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    Programme_Name_in_campus = models.CharField(max_length=255)
    Year_1_Programme_cost = models.CharField(max_length=255)
    _2022_cut_off = models.CharField(max_length=255)
    _2021_cut_off = models.CharField(max_length=255)
    _2020_cut_off = models.CharField(max_length=255)