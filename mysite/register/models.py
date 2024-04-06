from django.db import models
from django.contrib.auth.models import User

class QuestionnaireData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(verbose_name="Age")
    agp = models.IntegerField(verbose_name="Average Grade Points(KCSE points)")
    conscientiousness = models.IntegerField(verbose_name='Conscientiousness', choices=[(i, str(i)) for i in range(1, 6)])
    agreeableness = models.IntegerField(verbose_name='Agreeableness', choices=[(i, str(i)) for i in range(1, 6)])
    neuroticism = models.IntegerField(verbose_name='Neuroticism', choices=[(i, str(i)) for i in range(1, 6)])
    openness = models.IntegerField(verbose_name='Openness', choices=[(i, str(i)) for i in range(1, 6)])
    extroversion = models.IntegerField(verbose_name='Extroversion', choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"QuestionnaireData for user {self.user.username}"
