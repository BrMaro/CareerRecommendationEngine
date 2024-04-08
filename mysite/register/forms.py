from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import QuestionnaireData
from main.models import Course

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=200)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ["username", "gender", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields['gender'].label = "Gender"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"


class AuthenticationForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class QuestionnaireForm(forms.ModelForm):

    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    age = forms.IntegerField(label="Age", min_value=15, max_value=90)
    agp = forms.IntegerField(label="Average Grade Points(KCSE points)", min_value=0, max_value=84)

 
    conscientiousness = forms.ChoiceField(
        label='Conscientiousness',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The degree to which a person prefers to plan ahead rather than being spontaneous.",
        required=True
    )
    agreeableness = forms.ChoiceField(
        label='Agreeableness',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="How strongly a person tends to be kind, sympathetic, and helpful to others.",
        required=True

    )
    neuroticism = forms.ChoiceField(
        label='Neuroticism',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The extent to which someone is inclined to worry or be temperamental.",
        required=True

    )
    openness = forms.ChoiceField(
        label='Openness',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The extent to which a person has an appreciation for a variety of experiences.",
        required=True

    )
    extroversion = forms.ChoiceField(
        label='Extroversion',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The extent to which a person tends to prefer being sociable, outgoing, and talkative.",
        required=True
    )

    class Meta:
        model = QuestionnaireData  # Specify the model class
        fields = ['age', 'agp', 'conscientiousness', 'agreeableness', 'neuroticism', 'openness', 'extroversion']


class LockCoursesForm(forms.Form):
    locked_courses = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(LockCoursesForm, self).__init__(*args, **kwargs)
        # Populate queryset dynamically
        self.fields['locked_courses'].queryset = Course.objects.all()