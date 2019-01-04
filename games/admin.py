from django.contrib import admin
from .models import Player, Developer, Game, BoughtGame, Label

# Register your models here.
admin.site.register(Player)
admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(BoughtGame)
admin.site.register(Label)
