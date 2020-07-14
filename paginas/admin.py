from django.contrib import admin
from .models import steamuser, ligas, players_liga, liga_lobby, players_lobby
# sqlmigrate paginas 0001 see raw sql

admin.site.register(steamuser)
admin.site.register(players_liga)
admin.site.register(liga_lobby)
admin.site.register(players_lobby)
admin.site.register(ligas)



