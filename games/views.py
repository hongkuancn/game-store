from random import *
import string
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpResponse, Http404
import json
from django.http import JsonResponse

from .models import Developer, Player, Game, BoughtGame, Label, BestScore, GameState
from django.urls import reverse
from .models import Developer, Player, Game, BoughtGame, Label, Payment
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

    games = Game.objects.all()
    return render(request, "games/index.html", {'game_list': games})


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
    return redirect('games:index')

def inventory(request):
    user = get_object_or_404(User, pk=request.user.id)
    if user.developer:
        my_game_list = user.developer.developedgames.all()
        return render(request, "games/inventory.html", {'my_game_list': my_game_list})

def game_detail(request, game_id):

    game = get_object_or_404(Game, pk=game_id)

    # Generate random string for pid
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.digits
    rdmstr = "".join(choice(allchar)
                        for x in range(randint(min_char, max_char)))

    from hashlib import md5

    pid = '{}{}'.format(game.name, rdmstr)
    sid = '2333'
    amount = game.price
    secret_key = '786e1a1033b80aec7b150581c209be39'
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(
        pid, sid, amount, secret_key)

    # checksumstr is the string concatenated above
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()

    # if there is no such pid
    if not Payment.objects.filter(pid=pid).exists():
        Payment.objects.create(game=game, pid=pid).save()
        # TODO: if payment already exists, which page to go

    # checksum is the value that should be used in the payment request
    return render(request, "games/gaming.html", {'pid': pid, 'sid': sid, 'amount': amount, 'checksum': checksum, "game":game})

def player_game(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        if user.player:
            my_bought_game_list = user.player.boughtgame_set.all()
            return render(request, 'games/playersgames.html', {'my_bought_game_list': my_bought_game_list})

def payment_error(request):
    return render(request, "games/signup.html",)

def payment_cancel(request):
    return render(request, "games/login.html",)


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
                return render(request, "games/signup.html", {"error": "Username exists", "form": newForm})
                # reverse("games:signup")
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
                # Developer redirect to inventory page
                return redirect("games:inventory")
            elif userType == 'player':
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                player = Player.objects.create(user=user, balance=100).save()
                user.save()
                with mail.get_connection() as connection:
                    mail.EmailMessage("Thanks for your registration!", "Glorious! {}".format(
                        username), "hongkuan.wang@aalto.fi", [email], connection=connection,).send()
                login(request, user)
                return redirect("games:player_game")
    return redirect('games:index')

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
                if hasattr(user, 'developer'):
                    # Developer redirect to inventory page
                    return redirect("games:inventory")
                elif hasattr(user, 'player'):
                    return redirect("games:player_game")
    return redirect('games:index')

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

def gaming(request):
    response = {}
    if request.is_ajax():
        if request.method == 'POST':
            currentUser = request.user
            game = Game.objects.filter(pk=request.POST['id']).first()
            data = json.loads(request.POST['data'])
            messageType = data['messageType']
            if messageType == "SAVE":
                    gameState = data['gameState']
                    currentState = GameState(user=currentUser, game=game, game_state = gameState)
                    currentState.save()
                    response = {
                       'messageType':"SAVE",
                       'gameState':gameState
                    }
            elif messageType == "LOAD_REQUEST":
                    gameState = GameState.objects.filter(user=currentUser, game=game).values('game_state').last()
                    state = gameState['game_state']
                    response = {
                        'messageType':"LOAD",
                        'gameState':state
                    }
            elif messageType == "SCORE":
                    newScore = data['score']
                    bestScore = BestScore.objects.filter(user=currentUser, game=game).values("score").first()
                    newBestscore = BestScore(user=currentUser, game=game, score=newScore)
                    newBestscore.save()
                    scoreList = BestScore.objects.filter(game=game).order_by('-score')[:3]
                    bestScores = ""
                    for scores in scoreList:
                        bestScores = bestScores + "<tr><td>" + scores.user.username + "</td><td>" + str(scores.score) + "</td></tr>"
                    response = {
                        'messageType':"SCORE",
                        'bestScore': bestScores
                    }
            elif messageType == "ERROR":
                    response = {
                        'messageType':"ERROR",
                        'error': "There is an error"
                    }
    return JsonResponse(response)

    return redirect('games:index')

def payment_success(request):
    if request.user.is_authenticated:
        print(request.user.id)
        user = get_object_or_404(User, pk=request.user.id)
        print(user)
        player = user.player

        payment = get_object_or_404(Payment, pid=request.GET.get('pid'))
        game = payment.game

        if BoughtGame.objects.filter(user=player, game_info=game).exists():
            # TODO: Already bought the game
            return redirect('games:index')

        if player.balance >= game.price:
            BoughtGame.objects.create(user=player, game_info=game, best_score=0, price=game.price).save()
            player.balance = F('balance') - game.price
            game.sales = F('sales') + 1
            game.save()
            player.save()
            payment.delete()

        return redirect('games:index')
    else:
        return redirect('games:login')
