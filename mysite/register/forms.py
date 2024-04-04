from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

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
