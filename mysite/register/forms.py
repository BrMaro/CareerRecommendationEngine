from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
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


class QuestionnaireForm(forms.Form):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = forms.IntegerField(label="age")
    agp = forms.IntegerField(label="Average Grade Points(AGP)")
    # INTEREST_CHOICES = [
    # "Graphic Design", "Blogging", "Amateur Astronomy", "Cooking Classes", "Gardening",
    # "Homebrewing Coffee", "Magic Tricks", "Hiking", "Learning Languages", "Podcasting",
    # "Chess", "Photography", "Bird Watching", "Origami", "Archery", "Stand-up Comedy",
    # "Music Composition", "Pottery", "Calligraphy", "Running", "Yoga", "Tennis",
    # "Swimming", "Rock Climbing", "Cycling", "Badminton", "Chess Boxing", "Martial Arts",
    # "Sailing", "Rowing", "Archery", "Soccer", "Skiing", "Gymnastics", "Polo", "Kickboxing",
    # "Volleyball", "Basketball", "Drama Club", "Orchestra or Band", "Debate Team",
    # "Relay Races", "Volunteering Group", "Quiz Team", "Dance Troupe", "Rowing Crew",
    # "Chess Club", "Book Club", "Film-Making Group", "Chorale Group", "Tech Club",
    # "Competitive Gaming Team", "Environmental Conservation Group", "Innovation Lab",
    # "DIY Crafting Club", "Storm Chasing", "Beekeeping", "Falconry", "Underwater Hockey",
    # "Bonsai Cultivation", "Capoeira", "Ice Sculpting", "Parkour", "Astro-Photography",
    # "Ghost Hunting", "Acrobatics", "Competitive Eating", "Sand Sculpting", "Aerial Silks",
    # "LARPing", "Puppetry", "Cryptozoology", "Fencing", "Pyrography", "Skydiving",
    # "Analytical Hobbies And Interests", "Sudoku", "Programming", "Data Analysis",
    # "Reading Scientific Journals", "Cryptozoology", "Philosophical Debates", "Cryptography",
    # "Economic Forecasting", "Astronomy", "Birdwatching", "Genealogy", "Bridge",
    # "Model Building", "DIY Electronics", "Numismatics", "Technical Hobbies And Interests",
    # "Coding", "Robotics", "Computer Building", "Web Development", "Amateur Radio Operation",
    # "Photography & Photo Editing", "Software Beta Testing", "Video Production", "Advanced Excel",
    # "Game Development", "Home Networking", "Linux Administration", "Building Drones",
    # "3D Printing", "Data Analysis", "Cryptocurrency Trading", "Machine Learning Projects"
    # ]

    # interests = forms.MultipleChoiceField(
    #     choices=INTEREST_CHOICES,
    #     widget=forms.CheckboxSelectMultiple
    # )
    conscientiousness = forms.ChoiceField(
        label='Conscientiousness',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The degree to which a person prefers to plan ahead rather than being spontaneous."
    )
    agreeableness = forms.ChoiceField(
        label='Agreeableness',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="How strongly a person tends to be kind, sympathetic, and helpful to others."
    )
    neuroticism = forms.ChoiceField(
        label='Neuroticism',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The extent to which someone is inclined to worry or be temperamental."
    )
    openness = forms.ChoiceField(
        label='Openness',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The extent to which a person has an appreciation for a variety of experiences."
    )
    extroversion = forms.ChoiceField(
        label='Extroversion',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The extent to which a person tends to prefer being sociable, outgoing, and talkative."
    )