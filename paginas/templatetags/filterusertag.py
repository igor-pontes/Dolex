from django import template
from paginas.models import *
from django.shortcuts import redirect

register = template.Library()




@register.simple_tag
def isregistered(user, liga):
	is_registered = False
	user_id = user
	user = steamuser.objects.get(steamid=user_id)
	pl = user.players_liga_set.all().filter(liga=liga)
	if pl:
		is_registered = True

	return is_registered

@register.simple_tag
def liga_slots(liga):
	lens = len(liga.players_liga_set.all())
	return lens


@register.simple_tag
def lobby_filter(lobby, liga):
	lobby_players_counter = len(liga.liga_lobby_set.get(nome=lobby.nome).players_lobby_set.all())
	return lobby_players_counter


#{% with ''|center:0 as range %}{% for i in range %}{% endfor %}{% endwith %}
@register.simple_tag
def range_filter(number):
	return range(number)

@register.simple_tag
def lobbys_player(lobby, liga):
	lig = ligas.objects.get(slug = liga)
	lob = lig.liga_lobby_set.get(slug=lobby)
	players_c = len(lob.players_lobby_set.all())
	return players_c

@register.simple_tag
def lobby_player(key, lobby, liga):

	lig = ligas.objects.get(slug = liga)
	try:
		lob = lig.liga_lobby_set.get(slug=lobby)
	except liga_lobby.DoesNotExist:
		return redirect('/ligas/{}'.format(lobby))
	try:
		players_c = lob.players_lobby_set.get(slot=key)
	except players_lobby.DoesNotExist as e:
		players_c = 'lol'
	
	return players_c
	

