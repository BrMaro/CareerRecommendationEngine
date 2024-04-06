from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import RegisterForm
from .forms import QuestionnaireForm
from .models import QuestionnaireData


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
    user = request.user

    




    if QuestionnaireData.objects.filter(user=request.user).exists():
        print(f"{request.user} data already saved")
        return render(request, "register/recommendations.html")

    if request.method == "POST":
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            form = QuestionnaireForm(request.POST)
            questionnaire_data = form.save(commit=False)
            questionnaire_data.user = user  # Associate with the current user
            questionnaire_data.save()

            print("questionnaire_data saved to model")
            return render(request, "register/recommendations.html")

        else:
            print("invalid form")
            print(form.errors)  # Print the form errors for debugging
            messages.error(request, 'Invalid input. Please try again.')

            return render(request, "register/questionnaire.html",{'form': form})
    else:
        form = QuestionnaireForm()
        return render(request, 'register/questionnaire.html', {'form': form})
            

