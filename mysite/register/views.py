from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import RegisterForm
from .forms import QuestionnaireForm


# Create your views here.
def register(request):
    print("Is user authenticated:", request.user.is_authenticated)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = RegisterForm()
        return render(request, "register/register.html", {"form": form, "user": request.user})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                return redirect("/home")
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                
    else:
        form = AuthenticationForm()
    return render(request,"registration/login.html",{"form":form})


def logout_user(request):
    logout(request)
    return redirect("/home")  


def recommendations(request):
    if request.method == "POST":
        form = QuestionnaireForm(request,request.POST)
        if form.is_valid():
            data = form.cleaned_data
            questionnaire_data = QuestionnaireForm(
                user=request.user,
                age=data['age'],
                agp=data['agp'],
                interests=', '.join(data['interests']),
                conscientiousness=data['conscientiousness'],
                agreeableness=data['agreeableness'],
                neuroticism=data['neuroticism'],
                openness=data['openness'],
                extroversion=data['extroversion']
            )
            questionnaire_data.save()

            return render(request,"register/recommendations.html")
    else:
        form = QuestionnaireForm()
        return render(request, 'register/recommendations.html', {'form': form})
            

