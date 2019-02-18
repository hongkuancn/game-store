from random import *
import string
import json
import os
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, JsonResponse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage

from .models import Developer, Player, Game, BoughtGame, Label, Payment
from .forms import SignupForm, LoginForm, CreateNewGameForm

"""
GET handlers
"""
def index(request):
    if not Label.objects.filter(type='adventure').exists():
        l1 = Label.objects.create(type='adventure').save()
    if not Label.objects.filter(type='puzzle').exists():
        l2 = Label.objects.create(type='puzzle').save()
    if not Label.objects.filter(type='action').exists():
        l3 = Label.objects.create(type='action').save()
    if not Label.objects.filter(type='sports').exists():
        l3 = Label.objects.create(type='sports').save()
    if not Label.objects.filter(type='racing').exists():
        l3 = Label.objects.create(type='racing').save()
    if not Label.objects.filter(type='strategy').exists():
        l3 = Label.objects.create(type='strategy').save()
    if not Label.objects.filter(type='combat').exists():
        l3 = Label.objects.create(type='combat').save()
    if not Label.objects.filter(type='other').exists():
        l3 = Label.objects.create(type='other').save()

    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        if not hasattr(user, 'developer') and not hasattr(user, 'player'):
            return render(request, "games/sociallogin.html")

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

# show games created by a developer user
def inventory(request):
    user = get_object_or_404(User, pk=request.user.id)
    if hasattr(user, 'developer'):
        my_game_list = user.developer.developedgames.all()
        return render(request, "games/inventory.html", {'my_game_list': my_game_list})
    else:
        return redirect('games:index')


def show_game_with_category(request, category):
    label = get_object_or_404(Label, type=category)
    try:
        games = list(Game.objects.filter(label=label))
    except Game.DoesNotExist:
        games = []
    return render(request, "games/index.html", {'game_list': games})


def game_detail(request, game_id):

    game = get_object_or_404(Game, pk=game_id)
    bought = False
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        if hasattr(user, 'player'):
            if BoughtGame.objects.filter(user=user.player, game_info=game).exists():
                bought = True

    # Generate random string for pid
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.digits
    rdmstr = "".join(choice(allchar)
                        for x in range(randint(min_char, max_char)))

    from hashlib import md5

    pid = '{}{}'.format(rdmstr, game.id)
    # print(pid)
    sid = os.environ['PID']
    amount = game.price
    # print(amount)
    secret_key = os.environ['SECRET_KEY']
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(
        pid, sid, amount, secret_key)

    # checksumstr is the string concatenated above
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    # print(checksum)

    # if there is no such pid
    if not Payment.objects.filter(pid=pid).exists():
        Payment.objects.create(game=game, pid=pid).save()

    # checksum is the value that should be used in the payment request
    return render(request, "games/gaming.html", {'pid': pid, 'sid': sid, 'amount': amount, 'checksum': checksum, "game":game, "bought": bought})

# show games bought by a player user
def player_game(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        if hasattr(user, 'player'):
            my_bought_game_list = user.player.boughtgame_set.all()
            return render(request, 'games/playersgames.html', {'my_bought_game_list': my_bought_game_list})


def payment_error(request):
    return render(request, "games/signup.html",)


def payment_cancel(request):
    return redirect("games:index")


def show_modify_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.developer.user.id == request.user.id:
        name = game.name
        price = game.price
        url = game.url_link
        description = game.description
        game_picture = game.game_profile_picture
        label = game.label.type
        form = CreateNewGameForm(initial={'name': name, 'price': price, 'url': url, 'description': description, 'game_picture': game_picture })
        return render(request, "games/modifygame.html", {'form': form, 'id': game_id, 'label': label })
    return redirect("games:index")


def game_purchase_history(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.developer.user.id == request.user.id:
        try:
            game_history = list(BoughtGame.objects.filter(game_info=game))
        except BoughtGame.DoesNotExist:
            game_history = []
    return render(request, 'games/statistics.html', {'game_history': game_history})


def activate_user_account(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, "games/thanks.html", { 'message': 'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return render(request, "games/thanks.html", {'message': 'Activation link is invalid!'})

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
                user.is_active = False
                user.save()

                # Send confirmation Email
                current_site = get_current_site(request)
                mail_subject = 'Activate your game account.'
                message = render_to_string('games/activation.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()

                return render(request, "games/thanks.html", {'message': 'Please confirm your email address to complete the registration'})
            elif userType == 'player':
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                player = Player.objects.create(user=user, balance=100).save()
                user.is_active = False
                user.save()

                # Send confirmation Email
                current_site = get_current_site(request)
                mail_subject = 'Activate your game account.'
                message = render_to_string('games/activation.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()

                return render(request, "games/thanks.html", {'message': 'Please confirm your email address to complete the registration'})
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
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                if hasattr(user, 'developer'):
                    return redirect("games:inventory")
                elif hasattr(user, 'player'):
                    return redirect("games:player_game")
    return redirect('games:index')


def create_new_game(request):
    print('something wrong')
    if request.method == "POST":
        form = CreateNewGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            url = form.cleaned_data['url']
            description = form.cleaned_data['description']
            game_profile_picture = form.cleaned_data['game_picture']
            label = request.POST['label']
            developer = User.objects.get(pk=request.user.id).developer

            if Game.objects.filter(name=name).exists():
                newForm = CreateNewGameForm()
                return render(request, "games/newgame.html", {"error": "Same game name exists", "form": newForm})

            if name is not None and price is not None and url is not None and description is not None and label is not None and developer is not None and game_profile_picture is not None:
                if price >= 0:
                    l = get_object_or_404(Label, type=label)
                    game = Game.objects.create(name=name, price=int(price), url_link=url, description=description, developer=developer, game_profile_picture=game_profile_picture, label=l).save()
                else:
                    newForm = CreateNewGameForm()
                    return render(request, "games/newgame.html", {"error": "Price cannot be negative!", "form": newForm})
            else:
                newForm = CreateNewGameForm()
                return render(request, "games/newgame.html", {"error": "Required field should be filled", "form": newForm})
    return redirect("games:inventory")


def gaming(request):
    response = {}
    if request.is_ajax():
        if request.method == 'POST':
            currentUser = request.user.player
            game = Game.objects.filter(pk=request.POST['id']).first()
            data = json.loads(request.POST['data'])
            messageType = data['messageType']
            if messageType == "SAVE":
                preState = BoughtGame.objects.filter(user=currentUser, game_info=game).values('game_state').last()
                preGamestate = preState['game_state']
                gameState = data['gameState']
                newState = BoughtGame(user=currentUser, game_info=game, game_state=gameState)
                if preGamestate is None:
                    newState.save()
                else:
                    BoughtGame.objects.filter(user=currentUser, game_info=game).update(game_state=gameState)
                response = {
                    'messageType':"SAVE",
                    'gameState':gameState
                }
            elif messageType == "LOAD_REQUEST":
                gameState = BoughtGame.objects.filter(user=currentUser, game_info=game).values('game_state').last()
                state = gameState['game_state']
                response = {
                    'messageType':"LOAD",
                    'gameState':state
                }
            elif messageType == "SCORE":
                newScore = data['score']
                bestScore = BoughtGame.objects.filter(user=currentUser, game_info=game).values("best_score").last()
                preScore = bestScore['best_score']
                newBestscore = BoughtGame(user=currentUser, game_info=game, best_score=newScore)
                if preScore is None:
                    newBestscore.save()
                elif newScore > preScore:
                    BoughtGame.objects.filter(user=currentUser, game_info=game).update(best_score=newScore)
                scoreList = BoughtGame.objects.filter(game_info=game).order_by('-best_score')[:3]
                bestScores = ""
                for scores in scoreList:
                    bestScores = bestScores + "<tr><td>" + scores.user.user.username + "</td><td>" + str(scores.best_score) + "</td></tr>"
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


def payment_success(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        player = user.player

        payment = get_object_or_404(Payment, pid=request.GET.get('pid'))
        game = payment.game

        if BoughtGame.objects.filter(user=player, game_info=game).exists():
            return redirect('games:player_game')

        if player.balance >= game.price:
            BoughtGame.objects.create(user=player, game_info=game, best_score=0, price=game.price).save()
            player.balance = F('balance') - game.price
            game.sales = F('sales') + 1
            game.save()
            player.save()
            payment.delete()

        return redirect('games:player_game')
    else:
        return redirect('games:login')


def modify_game(request, game_id):
    if request.method == "POST":
        form = CreateNewGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            url = form.cleaned_data['url']
            game_profile_picture = form.cleaned_data['game_picture']
            description = form.cleaned_data['description']

            game = get_object_or_404(Game, pk=game_id)
            if game.developer.user.id == request.user.id:
                game.name = name
                game.price = price
                game.url = url
                game.description = description
                game.game_profile_picture = game_profile_picture
                game.save()
            return redirect("games:inventory")


def delete_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.developer.user.id == request.user.id:
        game.delete()
    return redirect("games:inventory")


def choose_type(request):
    if request.method == "POST":
        userType = request.POST['userType']

        user = get_object_or_404(User, pk=request.user.id)

        if userType != 'developer' and userType != 'player':
            return render(request, "games/sociallogin.html", {"error": "Bad guy!"})
        elif userType == 'developer':
            developer = Developer.objects.create(user=user).save()
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Developer redirect to inventory page
            return redirect("games:inventory")
        elif userType == 'player':
            player = Player.objects.create(user=user, balance=100).save()
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("games:player_game")
    return redirect('games:thanks')
