# Generated by Django 5.0 on 2024-02-15 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('programme_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('programme_name_in_campus', models.CharField(blank=True, db_column='Programme_Name_in_campus', max_length=255, null=True)),
                ('year_1_programme_cost', models.CharField(blank=True, db_column='Year_1_Programme_cost', max_length=255, null=True)),
                ('field_2022_cut_off', models.CharField(blank=True, db_column='_2022_cut_off', max_length=255, null=True)),
                ('field_2021_cut_off', models.CharField(blank=True, db_column='_2021_cut_off', max_length=255, null=True)),
                ('field_2020_cut_off', models.CharField(blank=True, db_column='_2020_cut_off', max_length=255, null=True)),
            ],
            options={
                'db_table': 'certification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('programme_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('cluster', models.CharField(blank=True, db_column='Cluster', max_length=255, null=True)),
                ('cluster_subject_1', models.CharField(blank=True, db_column='Cluster_subject_1', max_length=255, null=True)),
                ('cluster_subject_2', models.CharField(blank=True, db_column='Cluster_subject_2', max_length=255, null=True)),
                ('cluster_subject_3', models.CharField(blank=True, db_column='Cluster_subject_3', max_length=255, null=True)),
                ('cluster_subject_4', models.CharField(blank=True, db_column='Cluster_subject_4', max_length=255, null=True)),
                ('minimum_subject_1', models.CharField(blank=True, db_column='Minimum_subject_1', max_length=255, null=True)),
                ('minimum_subject_1_grade', models.CharField(blank=True, db_column='Minimum_subject_1_grade', max_length=255, null=True)),
                ('minimum_subject_2', models.CharField(blank=True, db_column='Minimum_subject_2', max_length=255, null=True)),
                ('minimum_subject_2_grade', models.CharField(blank=True, db_column='Minimum_subject_2_grade', max_length=255, null=True)),
                ('minimum_subject_3', models.CharField(blank=True, db_column='Minimum_subject_3', max_length=255, null=True)),
                ('minimum_subject_3_grade', models.CharField(blank=True, db_column='Minimum_subject_3_grade', max_length=255, null=True)),
                ('minimum_subject_4', models.CharField(blank=True, db_column='Minimum_subject_4', max_length=255, null=True)),
                ('minimum_subject_4_grade', models.CharField(blank=True, db_column='Minimum_subject_4_grade', max_length=255, null=True)),
                ('minimum_mean_grade', models.CharField(blank=True, db_column='Minimum_Mean_Grade', max_length=255, null=True)),
            ],
            options={
                'db_table': 'course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.IntegerField(blank=True, null=True)),
                ('alias', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('iname', models.CharField(db_column='IName', max_length=255, primary_key=True, serialize=False)),
                ('category', models.CharField(blank=True, db_column='Category', max_length=255, null=True)),
                ('institution_type', models.CharField(blank=True, max_length=255, null=True)),
                ('parent_ministry', models.CharField(blank=True, db_column='Parent_Ministry', max_length=255, null=True)),
            ],
            options={
                'db_table': 'institution',
                'managed': False,
            },
        ),
    ]