from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

#from django.contrib.auth.models import user

class steamuser(models.Model): #"Games" = database's table.
	steamid = models.CharField(max_length=200)
	nome = models.CharField(max_length=100)#nao coloquei parenteses para nao executar a funcao agr... so passando a funcao em si por enquanto
	avatar = models.TextField()
	avatarmedium = models.TextField()
	avatarfull = models.TextField()
	banido = models.BooleanField(default = False)

	def __str__(self):
		return self.nome

class ligas(models.Model):
	nome = models.CharField(default = None, max_length=100)
	desc = models.TextField(default=None)
	slug = models.CharField(default = None,max_length=110)
	date = models.DateTimeField(default=timezone.now)
	endate = models.DateTimeField(default=timezone.now)
	active = models.BooleanField(default = True)
	price = models.FloatField(default=0.0)
	slots = models.BigIntegerField(default=0)
	

	def __str__(self):
		return self.nome
class players_liga(models.Model):
	steamid = models.ForeignKey(steamuser, on_delete=models.CASCADE)
	pontos = models.BigIntegerField(default=1000)
	liga = models.ForeignKey(ligas, on_delete=models.CASCADE)
	active = models.BooleanField(default = True)
	def __str__(self):
		return self.steamid.nome

class liga_lobby(models.Model):
	ativo = models.BooleanField(default = False)
	nome = models.CharField(max_length=11)
	liga = models.ForeignKey(ligas, on_delete=models.CASCADE)
	slots = models.BigIntegerField(default=10)
	slug = models.CharField(default = None,max_length=110)
	lobbycriador = models.ForeignKey(steamuser, on_delete=models.CASCADE, default=None)
	bot = models.CharField(default=None, max_length=200)
	def __str__(self):
		return self.nome

class players_lobby(models.Model):
	steamid = models.ForeignKey(steamuser, on_delete=models.CASCADE)
	lobby = models.ForeignKey(liga_lobby, on_delete=models.CASCADE)
	time = models.CharField(max_length=3)
	slot = models.CharField(max_length=2, default=None)

	def __str__(self):
		return self.lobby.nome
		
		

	

