from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import Developer, Player
from .forms import SignupForm

"""
GET handlers
"""
def index(request):
    return render(request, "games/base.html")


def signup_page(request):
    if request.user.is_authenticated:
        return redirect("games:login")
    form = SignupForm()
    return render(request, "games/signup.html", {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("games:login")
    return render(request, "games/login.html")


def thanks(request):
    return render(request, "games/thanks.html")


def logout_user(request):
    logout(request)
    return render(request, "games/thanks.html")

"""
POST handlers
"""
def signup_user(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            userType = request.POST['userType']

            if password != password_confirmation:
                newForm = SignupForm()
                return render(request, "games/signup.html", {"error": "Passwords not match", "form": newForm})
            if User.objects.filter(email=email).exists():
                newForm = SignupForm()
                return render(request, "games/signup.html", {"error": "Email exists", "form": newForm})
            if User.objects.filter(username=username).exists():
                newForm = SignupForm()
                return render(request, "games/signup.html", {"error": "Username exists", "form": newForm})
            if userType != 'developer' and userType != 'player':
                newForm = SignupForm()
                return render(request, "games/signup.html", {"error": "Bad guy!", "form": newForm})
            elif userType == 'developer':
                user = User.objects.create_user(username=username, email=email, password=password)
                developer = Developer.objects.create(user=user).save()
                user.save()
                login(request, user)
                return redirect("games:index")
            elif userType == 'player':
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                player = Player.objects.create(user=user).save()
                user.save()
                login(request, user)
                return redirect("games:index")
    return render(request, "games/base.html")

def log_user_in(request):
    return render(request, "games/base.html")
