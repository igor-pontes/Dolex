import sys
from configparser import ConfigParser
from steam import SteamClient
from dota2 import Dota2Client
import logging
from random import randint
import os

#-> Mudar diretorio aqui se necessário
paginaspath = os.path.dirname(os.path.abspath(__file__))
botspath = os.path.join(paginaspath, 'bots.ini')

bot = ConfigParser()
bot.read(botspath)
############VARS###########
counterslot = 0
########BOTCONFIGS#########
bot_user = sys.argv[1]
bot_pass = sys.argv[2]
bot_sec = sys.argv[3]
lobby_name = sys.argv[4]
##########PLAYERS##########
#-Usar FOR aqui se quiser
player1 = int(sys.argv[5])#--------
player1time = sys.argv[6]
player2 = int(sys.argv[7])#--------
player2time = sys.argv[8]
player3 = int(sys.argv[9])#--------
player3time = sys.argv[10]
player4 = int(sys.argv[11])#--------
player4time = sys.argv[12]
player5 = int(sys.argv[13])#--------
player5time = sys.argv[14]
player6 = int(sys.argv[15])#--------
player6time = sys.argv[16]
player7 = int(sys.argv[17])#--------
player7time = sys.argv[18]
player8 = int(sys.argv[19])#--------
player8time = sys.argv[20]
player9 = int(sys.argv[21])#--------
player9time = sys.argv[22]
player10 = int(sys.argv[23])#--------
player10time = sys.argv[24]
############################

playerslot = {
	1: {
		'id': player1,
		'slot': None,
	},
	2:{
		'id': player2,
		'slot': None,
	},
	3:{
		'id': player3,
		'slot': None,
	},
	4:{
		'id': player4,
		'slot': None,
	},
	5:{
		'id': player5,
		'slot': None,
	},
	6:{
		'id': player6,
		'slot': None,
	},
	7:{
		'id': player7,
		'slot': None,
	},
	8:{
		'id': player8,
		'slot': None,
	},
	9:{
		'id': player9,
		'slot': None,
	},
	10:{
		'id': player10,
		'slot': None,
	},
}

############################
client = SteamClient()
dota = Dota2Client(client)
dota.verbose_debug = False

def converteridto32(steamid):
	cc = int(steamid) - 76561197960265728
	return cc



@client.on('logged_on')
def start_dota():
	dota.launch()
	print('Dota iniciou')

@dota.on('ready')
def create_dolex_lobby():
	global counterslot
	#bot[bot_sec]['estado'] = 'ocupado'
	#with open(botspath, 'w') as configfile:
	#	bot.write(configfile)
	bot_name = client.username
	pass_value = randint(0, 9999)
	dota.abandon_current_game()
	dota.leave_practice_lobby()
	dota.create_tournament_lobby(password=str(pass_value), tournament_game_id=None, tournament_id=0, options={
		'allow_cheats': False,
		'visibility': 0,
		'server_region': 10, #10-> Brazil
		'game_mode': 2, # 2-> CAPTAINS MODE, 1-> ALL PICK
		'game_name': lobby_name,
	})
	
	dota.sleep(1)
	dota.join_practice_lobby_team()
	dota.sleep(1)
	#Usar aqui FOR se quiser dps
	dota.invite_to_lobby(player1)
	dota.invite_to_lobby(player2)
	dota.invite_to_lobby(player3)
	dota.invite_to_lobby(player4)
	dota.invite_to_lobby(player5)
	dota.invite_to_lobby(player6)
	dota.invite_to_lobby(player7)
	dota.invite_to_lobby(player8)
	dota.invite_to_lobby(player9)
	dota.invite_to_lobby(player10)
	dota.channels.join_lobby_channel()

	bot[bot_sec]['chatipo'] = 'lobbycriado'
	bot[bot_sec]['conteudo'] = 'O bot criou a sala '+lobby_name+' com a seguinte senha: '+str(pass_value)+'.'
	with open(botspath, 'w') as configfile:
		bot.write(configfile)
	dota.sleep(1)
	bot[bot_sec]['chatipo'] = 'nada'
	bot[bot_sec]['conteudo'] = 'nada'
	with open(botspath, 'w') as configfile:
		bot.write(configfile)

	dota.sleep(9)
	if dota.lobby:
		if dota.channels.join_lobby_channel() is not None:
			lobby_chat = dota.channels.lobby
			lobby_chat.send('Obrigado por jogar na Dolex.')
		else:
			print('Nao foi possivel entrar no chat da lobby.')
	else:
		print('Nao foi possivel entrar na sala.')
	dota.sleep(1)
	for cont in range(0,180,+1):
		if cont is 0:
			dota.channels.lobby.send('Faltam 3 minutos para começar a partida')
		if cont is 60:
			dota.channels.lobby.send('Faltam 2 minutos para começar a partida')
		if cont is 120:
			dota.channels.lobby.send('Falta 1 minuto para começar a partida')
		if cont is 170:
			
			dota.channels.lobby.send('Partida começa em:')
			for n in range(10,0,-1):
				dota.channels.lobby.send(str(n))
				dota.sleep(1)
			for x in range(0, len(playerslot), +1):
				if playerslot[x+1]['slot'] is not None:
					counterslot += 1
				if playerslot[x+1]['slot'] is None:
					bot[bot_sec]['chatipo'] = 'banirplayerdapla'#'tirarpontosplayer'
					bot[bot_sec]['conteudo'] = str(playerslot[x+1]['id'])
					with open(botspath, 'w') as configfile:
						bot.write(configfile)
					dota.sleep(1)
			if counterslot == 10:	#dps '== 10'
				dota.launch_practice_lobby()
			elif counterslot < 10:
				bot[bot_sec]['estado'] = 'livre'
				bot[bot_sec]['comecou'] = 'nao'
				with open(botspath, 'w') as configfile:
					bot.write(configfile)
				dota.sleep(1)
				bot[bot_sec]['chatipo'] = 'playersnaoforamparaolobby'
				bot[bot_sec]['conteudo'] = 'O bot não conseguiu iniciar partida por falta de jogadores.'
				with open(botspath, 'w') as configfile:
					bot.write(configfile)
				dota.sleep(1)
				bot[bot_sec]['chatipo'] = 'nada'
				bot[bot_sec]['conteudo'] = 'nada'
				with open(botspath, 'w') as configfile:
					bot.write(configfile)
				dota.channels.lobby.send('Sem jogadores suficientes para começar partida.')
				dota.leave_practice_lobby()
				dota.sleep(1)
				dota.exit()
				exit()
			
		dota.sleep(1)
	
@dota.socache.on(('updated', dota.socache.ESOType.CSODOTALobby))
def lobby_match_update(obj):
	print('Algum lobby foi alterado...')
	if obj.match_outcome:
		if obj.match_outcome == 2:
			
			bot[bot_sec]['chatipo'] = 'radganhou'
			bot[bot_sec]['conteudo'] = 'O time Radiant ganhou.'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			dota.sleep(1)
			bot[bot_sec]['chatipo'] = 'nada'
			bot[bot_sec]['conteudo'] = 'nada'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)

			dota.sleep(1)

			dota.exit()
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()
			
		elif obj.match_outcome == 3:
			bot[bot_sec]['chatipo'] = 'dirganhou'
			bot[bot_sec]['conteudo'] = 'O time Dire ganhou.'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			dota.sleep(1)
			bot[bot_sec]['chatipo'] = 'nada'
			bot[bot_sec]['conteudo'] = 'nada'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)

			dota.sleep(1)
			
			dota.exit()
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()
		elif obj.match_outcome == 66:
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()

		elif obj.match_outcome == 68:
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()

		elif obj.match_outcome == 67:
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()

		elif obj.match_outcome == 0:
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()

		elif obj.match_outcome == 65:
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()

		elif obj.match_outcome == 64:
			bot[bot_sec]['comecou'] = 'nao'
			bot[bot_sec]['estado'] = 'livre'
			with open(botspath, 'w') as configfile:
				bot.write(configfile)
			client.sleep(1)
			exit()
########################################
# obj.match_outcome :
#  -DireVictory = 3
#  -NotScored_Canceled = 68
#  -NotScored_Leaver = 65
#  -NotScored_NeverStarted = 67
#  -NotScored_PoorNetworkConditions = 64
#  -NotScored_ServerCrash = 66
#  -RadVictory = 2
#  -Unknown = 0								
##########################################		
	if obj.members:
		global playerslot
		for i in range(len(obj.members)):
			# for aqui tbm depois se quiser
			if obj.members[i].id == player1:
				steam32 = converteridto32(player1)
				
				if player1time == 'rad':
					if obj.members[i].team == 0:
						playerslot[1]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[1]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[1]['slot'] = None
				elif player1time == 'dir':
					if obj.members[i].team == 1:
						playerslot[1]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[1]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[1]['slot'] = None

			if obj.members[i].id == player2:
				steam32 = converteridto32(player2)
				
				if player2time == 'rad':
					if obj.members[i].team == 0:
						playerslot[2]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[2]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[2]['slot'] = None
				elif player2time == 'dir':
					if obj.members[i].team == 1:
						playerslot[2]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[2]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[2]['slot'] = None
			
			if obj.members[i].id == player3:
				steam32 = converteridto32(player3)
				
				if player3time == 'rad':
					if obj.members[i].team == 0:
						playerslot[3]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[3]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[3]['slot'] = None
				elif player3time == 'dir':
					if obj.members[i].team == 1:
						playerslot[3]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[3]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[3]['slot'] = None
			if obj.members[i].id == player4:
				steam32 = converteridto32(player4)
				
				if player4time == 'rad':
					if obj.members[i].team == 0:
						playerslot[4]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[4]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[4]['slot'] = None
				elif player4time == 'dir':
					if obj.members[i].team == 1:
						playerslot[4]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[4]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[4]['slot'] = None
			if obj.members[i].id == player5:
				steam32 = converteridto32(player5)
				
				if player5time == 'rad':
					if obj.members[i].team == 0:
						playerslot[5]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[5]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[5]['slot'] = None
				elif player5time == 'dir':
					if obj.members[i].team == 1:
						playerslot[5]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[5]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[5]['slot'] = None
			if obj.members[i].id == player6:
				steam32 = converteridto32(player6)
				
				if player6time == 'rad':
					if obj.members[i].team == 0:
						playerslot[6]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[6]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[6]['slot'] = None
				elif player6time == 'dir':
					if obj.members[i].team == 1:
						playerslot[6]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[6]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[6]['slot'] = None
			if obj.members[i].id == player7:
				steam32 = converteridto32(player7)
				
				if player7time == 'rad':
					if obj.members[i].team == 0:
						playerslot[7]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[7]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[7]['slot'] = None
				elif player7time == 'dir':
					if obj.members[i].team == 1:
						playerslot[7]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[7]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[7]['slot'] = None
			if obj.members[i].id == player8:
				steam32 = converteridto32(player8)
				
				if player8time == 'rad':
					if obj.members[i].team == 0:
						playerslot[8]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[8]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[8]['slot'] = None
				elif player8time == 'dir':
					if obj.members[i].team == 1:
						playerslot[8]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[8]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[8]['slot'] = None
			if obj.members[i].id == player9:
				steam32 = converteridto32(player9)
				
				if player9time == 'rad':
					if obj.members[i].team == 0:
						playerslot[9]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[9]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[9]['slot'] = None
				elif player9time == 'dir':
					if obj.members[i].team == 1:
						playerslot[9]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[9]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[9]['slot'] = None
			if obj.members[i].id == player10:
				steam32 = converteridto32(player10)
				
				if player10time == 'rad':
					if obj.members[i].team == 0:
						playerslot[10]['slot'] = obj.members[i].name
					if obj.members[i].team == 1:
						playerslot[10]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[10]['slot'] = None
				elif player10time == 'dir':
					if obj.members[i].team == 1:
						playerslot[10]['slot'] = obj.members[i].name
					if obj.members[i].team == 0:
						playerslot[10]['slot'] = None
						dota.practice_lobby_kick(account_id=steam32)
					if obj.members[i].team == 4:
						playerslot[10]['slot'] = None
			
			


client.cli_login(username=bot_user, password=bot_pass)
client.run_forever()


