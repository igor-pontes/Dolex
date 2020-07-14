from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
import steamauth
from django.utils.safestring import mark_safe
import math
import urllib, json
from django.template.defaultfilters import slugify
from paginas.models import steamuser, ligas, players_liga, liga_lobby, players_lobby
from random import randint


def pag_liga_lobby_entrar(request, liga, lobby):

	if 'logged' in request.session :
		title = {'sitetitle': 'Home'}
		return render(request, 'dolex/home.html', title)
	else:
		title = {'sitetitle': 'Home'}
		return render(request, 'dolex/home.html', title)




def pag_criar_lobby(request, liga):
	if 'logged' in request.session :
		usernome = request.session['name']
		userid = request.session['steamid']
		useri = steamuser.objects.get(steamid = userid)
		if useri.banido is False:
		
			try:
				lig = ligas.objects.get(slug=liga)
			except ligas.DoesNotExist:
				return redirect('/ligas/')
			try:
				_liga = lig.players_liga_set.all().filter(steamid = useri)
			except ligas.DoesNotExist:
				return redirect('/ligas/')

			if _liga:

				nomelobby = random_name = 'Dolex#' + str(randint(0000, 9999))
				lslug = nomelobby.replace("#", "")
				criarlobby = liga_lobby(nome=nomelobby, liga=lig, slug=lslug, lobbycriador=useri, bot='nt')
				criarlobby.save()
				lobby_id = lig.liga_lobby_set.get(nome=nomelobby)
				registerplayerinlobby = players_lobby(steamid=useri, lobby=lobby_id, time='rad', slot=1)
				registerplayerinlobby.save()
				if criarlobby and registerplayerinlobby:
					return redirect('/liga/{}/lobby/{}'.format(liga, lslug))
				else:
					print('Erro ao criar lobby ou jogador(criador do lobby)')
			else:
				return redirect('/ligas/')
		else:
			return redirect('/')


	else:
		title = {'sitetitle': 'Home'}
		return render(request, 'dolex/home.html', title)


def pag_liga_lobby(request, liga):
	return redirect('/liga/{}'.format(liga))

def pag_liga_lobby_page(request, liga, lobby):
	if 'logged' in request.session :
		#lig = ligas.objects.get(slug=liga)
		#lob = lib.liga_lobby_set.get(slug=lobby)
		#if lob.ativo:
		userid = request.session['steamid']
		_user = steamuser.objects.get(steamid=userid)
		if _user.banido is False:
			try:
				lig = ligas.objects.get(slug=liga)
			except ligas.DoesNotExist:
				return redirect('/ligas/')
			if lig:
				try:
					liga_u = lig.players_liga_set.get(steamid=_user) 
				except players_liga.DoesNotExist:
					return redirect('/liga/{}'.format(liga))
				if liga_u:
					try:
						lob = lig.liga_lobby_set.get(slug=lobby)
					except liga_lobby.DoesNotExist:
						return redirect('/liga/{}'.format(liga))
					if lob:
						try:
							lobbynome = lig.liga_lobby_set.get(slug=lobby).nome
							lobbycriador = lig.liga_lobby_set.get(slug=lobby).lobbycriador.nome
						except liga_lobby.DoesNotExist:
							return redirect('/liga/{}'.format(liga))
						data = {'sitetitle': 'Lobby',
						'lobbynome':lobbynome,
						'lobby': lobby,
						'liganame': liga,
						'criadordolobby': lobbycriador,
						}
						return render(request, 'dolex/lobby.html', data)
			else:
				return redirect('/ligas/')
		else:
			return redirect('/')
		
	else:
		title = {'sitetitle': 'Home'}
		return render(request, 'dolex/home.html', title)


def index(request):
	if 'logged' in request.session :
		user_session = request.session['name']
		userid = request.session['steamid']
		uuserr = steamuser.objects.get(steamid=userid)
		if uuserr.banido is False:
			
			title = {
				'sitetitle': 'Home',
				'usuario': mark_safe(json.dumps(user_session))	
			}
			return render(request, 'dolex/home.html', title) #title will be just 'sitetile'
		else:
			title = {
				'sitetitle': 'Banido',
			}
			return render(request, 'dolex/banido.html', title)
	else:
		title = {'sitetitle': 'Home'}
		return render(request, 'dolex/home.html', title) #title will be just 'sitetile'

def login(request):
	return steamauth.auth('/process', False)

def logout(request):
	request.session.clear()
	return redirect('/')


def pag_liga_ranking(request, liga):
	if 'logged' in request.session:
		user__ = request.session['steamid']
		___user = steamuser.objects.get(steamid=user__)
		if ___user.banido is False:
			try: 
				liga = ligas.objects.get(slug=liga)
			except ligas.DoesNotExist:
				return redirect('/ligas/')
			players = liga.players_liga_set.all().order_by('-pontos')
			data={
				'sitetitle': 'Ligas',
				'liga': liga,
				'players': players
			}
			return render(request, 'dolex/ranking.html', data)
		else:
			return redirect('/')	
	else:
		return redirect('/')

def handler404(request, exception):
	data = {
		'sitetitle': '404'
	}
	return render(request, 'dolex/404.html', data)

def pag_liga_entrar(request, liga):
	if 'logged' in request.session:
		user__ = request.session['steamid']
		___user = steamuser.objects.get(steamid=user__)
		if ___user.banido is False:
			try:
				liga__ = ligas.objects.get(slug=liga)
			except ligas.DoesNotExist:
				return redirect('/ligas/')
			print(len(liga__.players_liga_set.filter(steamid =___user)))
			if len(liga__.players_liga_set.filter(steamid =___user)) == 0:
				try:
					liga_ = ligas.objects.get(slug=liga)
				except ligas.DoesNotExist:
					return redirect('/ligas/')
				lic_ = len(liga_.players_liga_set.all())
				if lic_ == liga_.slots and liga_.slots != 0:
					return redirect('/liga/{}'.format(liga_.slug))
				else:
					if liga_.active is True:
						user = request.session['steamid']
						_user = steamuser.objects.get(steamid=user)
						_nome = request.session['name']
						__user = players_liga(steamid=_user, liga=liga_)
						__user.save()
						if __user:
							return redirect('/liga/{}'.format(liga_.slug))
						else:
							return redirect('/')
					else:
						return redirect('/ligas')
			else:
				return redirect('/liga/{}'.format(liga__.slug))
		else:
			return redirect('/')
	else:
		return redirect('/')


def pag_liga_sair(request, liga):
	if 'logged' in request.session:
		try:
			liga_ = ligas.objects.get(slug=liga)
		except:
			return redirect('/ligas/')
		user = request.session['steamid']
		_user = steamuser.objects.get(steamid=user)
		try: 
			pla = players_liga.objects.get(steamid=_user, liga=liga_)
		except players_liga.DoesNotExist:
			return redirect('/liga/{}'.format(liga_.slug))
		if pla:
			if liga_.active is True:
				pla.delete()
			else:
				return redirect('/ligas/')
		return redirect('/ligas/')

	else:
		return redirect('/')


def pag_ligas(request, start=None):
	if start is not None:
		if 'logged' in request.session:
			page = start
			limit = 5
			start = start - 1
			start = start * limit
			user_id = request.session['steamid']
			_user = steamuser.objects.get(steamid=user_id)
			if _user.banido is False:
				liga = ligas.objects.order_by('slots')[start:start+limit]
				_ligas = ligas.objects.all()

				cc = math.ceil(len(_ligas)/limit)


				title = {
					'sitetitle': 'Ligas',
					'ligas': liga,
					'cc': cc,
					'lol': len(liga),
					'page': page
				}
				return render(request, 'dolex/ligas.html', title)
			else:
				return redirect('/')
		else:
			return redirect('/')
	else:
		return redirect('/ligas/1')

def pag_liga(request, liga=None):
	if liga is not None:
		try:
			query = ligas.objects.get(slug=liga)
		except ligas.DoesNotExist:
			query = None
		if query is not None:
			if query.active is not False:
				if 'logged' in request.session:
					registered = False
					user_id = request.session['steamid']
					user = steamuser.objects.get(steamid=user_id)
					if user.banido is False:
						lig = ligas.objects.get(slug=liga)
						try:
							query = players_liga.objects.get(steamid=user, liga=lig)
						except players_liga.DoesNotExist:
							query = None
						if query is not None:
							if query.liga == lig:
								registered = True
							else:
								pass
							#	plslig = players_liga(steamid=user, liga=lig)
							#	plslig.save()	
						else:
							pass
						lic = len(ligas.objects.get(slug=liga).players_liga_set.all())
						lobby = liga_lobby.objects.filter(liga = lig)

						data = {
						'ureg': registered,
						'sitetitle': 'Ligas',
						'liga': ligas.objects.get(slug=liga),
						'c': lic,
						'lobbysc': len(lobby),
						'ligaName': mark_safe(json.dumps(liga)),
						'loby': lobby

						}
						return render(request, 'dolex/liga.html', data)
					else:
						return redirect('/')
				else:
					return redirect('/')
			else:
				return redirect('/ligas')
		else:
			return redirect('/ligas')
	else:
		return redirect('/ligas')
def process_login(request):
	steam_id = steamauth.get_uid(request.GET)
	steam_key = '501A831836E1F00409A77278F9C926B7'

	if steam_id is not False:
		#j = json.loads('{"one" : "1", "two" : "2", "three" : "3"}')
		profile_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+ steam_key +'&steamids='+str(steam_id)
		response = urllib.request.urlopen(profile_url)
		user_json = json.loads(response.read())
		user = user_json['response']['players'][0]
		__user = user['steamid']
		__nome = user['personaname']
		__purl = user['profileurl']
		__avatar = user['avatar']
		__avatarmedium = user['avatarmedium']
		__avatarfull = user['avatarfull']
		request.session['steamid'] = user['steamid']
		request.session['name'] = user['personaname']
		request.session['profileurl'] = user['profileurl']
		request.session['avatar'] = user['avatar']
		request.session['avatarmedium'] = user['avatarmedium']
		request.session['avatarfull'] = user['avatarfull']
		request.session['logged'] = True
		try:
			user = steamuser.objects.get(steamid=request.session['steamid'])
		except steamuser.DoesNotExist:
			user = None
		if user is not None:
			if user.nome != request.session['name']:
				user.nome = request.session['name']
				user.save()
			elif user.avatar != request.session['avatar']:
				user.avatar = request.session['avatar']
				user.save()
			elif user.avatarmedium != request.session['avatarmedium']:
				user.avatarmedium = request.session['avatarmedium']
				user.save()
			elif user.avatarfull != request.session['avatarfull']:
				user.avatarfull = request.session['avatarfull']
				user.save()
			else:
				pass
		else:
			pass

		request.session.set_expiry(30000)

		try:
			query = steamuser.objects.get(steamid = steam_id)
		except steamuser.DoesNotExist:
			query = None

		if query is None:
			s_user = steamuser(steamid=__user, nome=__nome, avatar=__avatar, avatarmedium=__avatarmedium, avatarfull=__avatarfull)
			s_user.save()
		else:
			pass

		return redirect('/')
	else: 
		return redirect('/')

def sobre(request):
	title = {'sitetitle': 'Sobre'}
	return render(request, 'dolex/sobre.html', title)
