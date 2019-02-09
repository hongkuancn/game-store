from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.


class Player(models.Model):
    """
    id - automatic
    username - CharField
    email - EmailField
    password - CharField
    bought_games - p1.boughtgame_set.all()
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=100, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.user.username


class Developer(models.Model):
    """
    id - automatic
    username - CharField
    email - EmailField
    password - CharField ?
    developed_games - d1.developedgames_set.all()
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Label(models.Model):
    """
    type - CharField
    """
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ('type',)


class Game(models.Model):
    """
    id - automatic
    name - CharField
    price - IntegerField ?
    bought_players - point to Player class  ???
    labels - CharField ?
    game_profile_picture - ImageField
    description - TextField
    developer - point to Developer class
    url_link - URLField   !!!
    """

    name = models.CharField(max_length=50,unique=True,blank=True)
    developer = models.ForeignKey(
        Developer, on_delete=models.CASCADE, related_name='developedgames')
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    game_profile_picture = models.CharField(max_length=150)
    url_link = models.URLField()
    description = models.TextField()
    # label = models.ManyToManyField(Label)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, default=1)
    sales = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class BoughtGame(models.Model):
    """
    user - point to Player class
    game_info - point to Game class
    bought_time - DateField
    best_score - IntegerField
    game_state - JSONField
    """
    user = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True)
    game_info = models.ForeignKey(Game, on_delete=models.CASCADE)
    bought_time = models.DateTimeField(default=timezone.now)
    best_score = models.IntegerField(default=0)
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return '{} bought {}'.format(self.user.user.username, self.game_info.name)


class Payment(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    pid = models.CharField(max_length=50)
