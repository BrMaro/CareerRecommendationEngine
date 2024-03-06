from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import RegisterForm


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
        
        # if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect("/home")
        else:
            messages.error(request, "Error Logging In. Try again.")
            return redirect("/login")
    else:
        form=RegisterForm()
    return render(request,"registration/login.html",{"form":form})



def logout_user(request):
    logout(request)
    return redirect("/home")  
