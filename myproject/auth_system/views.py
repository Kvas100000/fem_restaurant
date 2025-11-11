from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate,logout as auth_logout
from django.contrib import messages



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")


    else:
        form = CustomUserCreationForm()
    context = {"form": form}

    return render(request,"auth_system/register.html", context=context)



def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth_login(request, user)
                return redirect("index")
        else:
            messages.error(request, "Неправильный логин или пароль")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "auth_system/login.html", context=context)


def logout(request):
    auth_logout(request)
    return redirect('index')

