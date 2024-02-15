from django.db import models

# Create your models here.

class Institution(models.Model):
    id = models.IntegerField(blank=True, null=True)
    alias = models.CharField(unique=True, max_length=255, blank=True, null=True)
    iname = models.CharField(db_column='IName', primary_key=True, max_length=255)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)  # Field name made lowercase.
    institution_type = models.CharField(max_length=255, blank=True, null=True)
    parent_ministry = models.CharField(db_column='Parent_Ministry', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'institution'


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    programme_name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    cluster = models.CharField(db_column='Cluster', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cluster_subject_1 = models.CharField(db_column='Cluster_subject_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cluster_subject_2 = models.CharField(db_column='Cluster_subject_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cluster_subject_3 = models.CharField(db_column='Cluster_subject_3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cluster_subject_4 = models.CharField(db_column='Cluster_subject_4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_1 = models.CharField(db_column='Minimum_subject_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_1_grade = models.CharField(db_column='Minimum_subject_1_grade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_2 = models.CharField(db_column='Minimum_subject_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_2_grade = models.CharField(db_column='Minimum_subject_2_grade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_3 = models.CharField(db_column='Minimum_subject_3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_3_grade = models.CharField(db_column='Minimum_subject_3_grade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_4 = models.CharField(db_column='Minimum_subject_4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_subject_4_grade = models.CharField(db_column='Minimum_subject_4_grade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimum_mean_grade = models.CharField(db_column='Minimum_Mean_Grade', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course'
class Certification(models.Model):
    programme_code = models.CharField(primary_key=True, max_length=255)
    iname = models.ForeignKey(Institution, models.DO_NOTHING, db_column='Iname', blank=True, null=True)  # Field name made lowercase.
    programme_name = models.ForeignKey(Course, models.DO_NOTHING, db_column='Programme_name', to_field='programme_name', blank=True, null=True)  # Field name made lowercase.
    programme_name_in_campus = models.CharField(db_column='Programme_Name_in_campus', max_length=255, blank=True, null=True)  # Field name made lowercase.
    year_1_programme_cost = models.CharField(db_column='Year_1_Programme_cost', max_length=255, blank=True, null=True)  # Field name made lowercase.
    field_2022_cut_off = models.CharField(db_column='_2022_cut_off', max_length=255, blank=True, null=True)  # Field renamed because it started with '_'.
    field_2021_cut_off = models.CharField(db_column='_2021_cut_off', max_length=255, blank=True, null=True)  # Field renamed because it started with '_'.
    field_2020_cut_off = models.CharField(db_column='_2020_cut_off', max_length=255, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'certification'