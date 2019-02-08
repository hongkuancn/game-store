from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpResponse, Http404

from .models import Developer, Player, Game, BoughtGame, Label
from .forms import SignupForm, LoginForm, CreateNewGameForm

"""
GET handlers
"""
def index(request):
    # TODO: where to initial the three instances
    if not Label.objects.filter(type='adventure').exists():
        l1 = Label.objects.create(type='adventure').save()
    if not Label.objects.filter(type='puzzle').exists():
        l2 = Label.objects.create(type='puzzle').save()
    if not Label.objects.filter(type='action').exists():
        l3 = Label.objects.create(type='action').save()
    return render(request, "games/base.html")


def signup_page(request):
    if request.user.is_authenticated:
        return redirect("games:thanks")
    form = SignupForm()
    return render(request, "games/signup.html", {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("games:thanks")
    form = LoginForm()
    return render(request, "games/login.html", {'form': form})


def thanks(request):
    return render(request, "games/thanks.html")

def newgame_page(request):
    form = CreateNewGameForm()
    return render(request, "games/newgame.html", {'form': form})

def logout_user(request):
    logout(request)
    return render(request, "games/base.html")

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
                with mail.get_connection() as connection:
                    mail.EmailMessage("Thanks for your registration!", "Glorious! {}".format(username), "hongkuan.wang@aalto.fi", [email], connection=connection,).send()
                login(request, user)
                return redirect("games:index")
            elif userType == 'player':
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                player = Player.objects.create(user=user).save()
                user.save()
                with mail.get_connection() as connection:
                    mail.EmailMessage("Thanks for your registration!", "Glorious! {}".format(
                        username), "hongkuan.wang@aalto.fi", [email], connection=connection,).send()
                login(request, user)
                return redirect("games:index")
    return render(request, "games/base.html")

def log_user_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is None:
                newForm = LoginForm()
                return render(request, "games/login.html", {"error": "User doesn't exists", "form": newForm})
            else:
                login(request, user)
                return redirect("games:index")
    return render(request, "games/base.html")

def create_new_game(request):
    if request.method == "POST":
        form = CreateNewGameForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            url = form.cleaned_data['url']
            description = form.cleaned_data['description']
            label = request.POST['label']
            # image = request.FILES['image']
            developer = User.objects.get(pk=request.user.id).developer

            if Game.objects.filter(name=name).exists():
                newForm = CreateNewGameForm()
                return render(request, "games/newgame.html", {"error": "Same game name exists", "form": newForm})

            if name is not None and price is not None and url is not None and description is not None and label is not None and developer is not None:
            # if Label.objects.filter(type=label).exists():
                l = get_object_or_404(Label, type=label)
                game = Game.objects.create(name=name, price=price, url_link=url, description=description, developer=developer, label=l).save()
            # else:
            #     new_label = Label.objects.create(type=label)
            #     new_label.save()
            #     game = Game.objects.create(name=name, price=price, url_link=url, description=description, developer=developer, label=new_label).save()
            else:
                newForm = CreateNewGameForm()
                return render(request, "games/newgame.html", {"error": "Required field should be filled", "form": newForm})
    return render(request, "games/base.html")

def gaming(request, game_id):
    try:
         game = Game.objects.get(pk = game_id)
    except Game.DoesNotExist:
         raise Http404("Game does not exist")
    return render(request, "games/gaming.html", {"game":game})

def games(request):
    return render(request, "games/gaming.html")