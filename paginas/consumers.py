from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from paginas.models import *
from configparser import ConfigParser
import os
from django.core.files import File
from steam import SteamClient
from dota2 import Dota2Client 
import logging
from random import randint
import subprocess
from asgiref.sync import async_to_sync

class LobbyConsumer(AsyncWebsocketConsumer):
    

    async def connect(self):
        self.lobbynome = self.scope['url_route']['kwargs']['lobbyslug']
        self.slugliga = self.scope['url_route']['kwargs']['ligaName']
        
        self.userr = self.scope["session"]["steamid"]
        #print(self.userr)
        # nome da lobby...
        #print(self.lobbynome)
        await self.channel_layer.group_add(
            self.lobbynome,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.lobbynome,
            self.channel_name
        )

    #when django receives data from javascript websocket!
    async def receive(self, text_data): 
        data = json.loads(text_data)
        lobbyslug = data['lobbyslug']
        _liga = data['liganame']
        tipodemensagem = data['tipo']
        if tipodemensagem == 'verificarjogador':
            _usuario = data['user']
            #print(_usuario)
            ver_jog = await self.verificasejogadorcriouliga(usuario = _usuario, liga=_liga, lobby = lobbyslug)
            if ver_jog is True:
                
                await self.channel_layer.group_send(
                    self.lobbynome,
                    {
                        'type': 'mcriou_lobby',
                        'mensagem': 'crioulobby'
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.lobbynome,
                    {
                        'type': 'mcriou_lobby',
                        'mensagem': 'naocrioulobby'
                    }
                )
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot2':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=2)
            #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=2)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot2',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        )
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='rad', slot=2, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot2',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot1':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=1)
            #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=1)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot1',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        ) 
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='rad', slot=1, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot1',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot3':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=3)
            #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=3)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot3',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        )    
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='rad', slot=3, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot3',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot4':

            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=4)
            #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=4)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot4',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        )
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='rad', slot=4, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot4',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot5':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=5)
                #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=5)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot5',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        ) 
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='rad', slot=5, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot5',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar

                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot6':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=6)
                #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=6)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot6',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        ) 
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='dir', slot=6, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot6',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar

                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot7':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=7)
                #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=7)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot7',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        ) 
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='dir', slot=7, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot7',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar

                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot8':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=8)
                #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=8)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot8',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        ) 
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='dir', slot=8, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot8',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar

                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot9':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=9)
                #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=9)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot9',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        ) 
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='dir', slot=9, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot9',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar

                            }
                        )
                else:
                    pass
            else:
                pass
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'ocuparslot10':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaa, lobby=lobbyy)
            if lobbystatus is False:
                
                versealguemestanoslot = await self.verificarslot(liga=ligaa, lobby=lobbyy, slot=10)
                #print(versealguemestanoslot)
                if versealguemestanoslot is False:
                    ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
                    #print(ver_se_jog_e_cad)
                    if ver_se_jog_e_cad is True:
                        getlobby = await self.getlobby(lobby=lobbyy, liga=ligaa)
                        slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa)  
                        atualizarslot = await self.atualizarslotlobbyplayer(user=usuario, liga=ligaa, lobby=lobbyy, slot=10)
                        #print(slot_ant)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot10',
                                'lobant': slot_ant,
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar
                            }
                        ) 
                    else:
                        cad_usuario = await self.cadastrarjogadornalobby(time='dir', slot=10, usuario = usuario, liga = ligaa, lobby = lobbyy)
                        _usuario = await self.getuserdata(user = usuario)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'ocuparslot10',
                                'user': _usuario.nome,
                                'avatar': _usuario.avatar

                            }
                        )
                else:
                    pass
            else:
                pass
                #await self.channel_layer.group_send(
                #    self.lobbynome,
                #    {
                #        'type': 'comecarchat',
                #        'mensagem': 'naopodetrocarslot',
                #        'botname': botname,
                #        'conteudo': 'Não se troca de slot ao início da partida.',
                #        
                #    }
                #)
#------------------------------------------------------------------------------------------
        elif tipodemensagem == 'chat':
            uuserr = data['user_chat']
            mensagem_chat = data['message_chat']
            await self.channel_layer.group_send(
                self.lobbynome,
                {
                    'type': 'chatmessage',
                    'mensagem': mensagem_chat,
                    'user': uuserr,

                }
            )

        elif tipodemensagem == 'saidalobby':
            usuario = data['user']
            lobbyy = data['lobbyslug']
            ligaa = data['liganame']
            ver_se_jog_e_cad = await self.verificasejogadorecadastrado(usuario = usuario, liga = ligaa, lobby = lobbyy)
            if ver_se_jog_e_cad is True:
                slot_ant = await self.pegarslotantigo(user=usuario, lobby=lobbyy, liga=ligaa) 
                deletar = await self.deletajogadordalobby(user=usuario, lobby=lobbyy, liga=ligaa)
                verificaseestavazio  = await self.verificalobbyvazio(lobby=lobbyy, liga=ligaa)
                #print(verificaseestavazio)
                if verificaseestavazio is True:
                    verificaseplayereocriador = await self.verificacriadordolobby(liga=ligaa, lobby=lobbyy, usuario=usuario)
                    if verificaseplayereocriador is True:
                        deletelobby = await self.deletarlobby(lobby = lobbyy, liga=ligaa)
                        

                    else:
                        deletelobby = await self.deletarlobby(lobby = lobbyy, liga=ligaa)

                else:
                    verificaseplayereocriador = await self.verificacriadordolobby(liga=ligaa, lobby=lobbyy, usuario=usuario)
                    if verificaseplayereocriador is True:
                        deletelobby = await self.deletarlobby(lobby = lobbyy, liga=ligaa)
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attlobby',
                                'mensagem': 'adminquitou',
                                'ultposi': slot_ant,

                            }
                        )
                        #manda mensagem falando q o lobby foi apagado
                    else:
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'attslot',
                                'mensagem': 'playerquitou',
                                'ultposi': slot_ant,

                            }
                        )
                    

            else:
                pass


        elif tipodemensagem == 'refreshbot':
            paginaspath = os.path.dirname(os.path.abspath(__file__))
            botspath = os.path.join(paginaspath, 'bots.ini')
            botname = '<Dolex>'
            lobbyslug = data['lobbyslug']
            directoryfiles = '/home/dolexadmin/dolex/paginas/'
            ligaslug = data['liganame']
            botdasala = await self.getbotdasala(liga=ligaslug, lobby=lobbyslug)
            if botdasala != 'nt':
                
                bot = ConfigParser()
                bot.read(botspath)
                if bot[botdasala]['chatipo'] == 'nada' and bot[botdasala]['conteudo'] == 'nada':
                    
                    pass
                elif bot[botdasala]['chatipo'] != 'nada' and bot[botdasala]['conteudo'] != 'nada':
                    
                    if bot[botdasala]['chatipo'] == 'lobbycriado':
                        if bot[botdasala]['comecou'] == 'nao':
                            bot[botdasala]['comecou'] = 'sim'
                            with open(botspath, 'w') as configfile:
                                bot.write(configfile)
                            mensagem = bot[botdasala]['conteudo']
                            await self.channel_layer.group_send(
                                self.lobbynome,
                                {
                                    'type': 'comecarchat',
                                    'mensagem': 'lobbycriadonodota',
                                    'botname': botname,
                                    'conteudo': mensagem,
                                }
                            )
                        if bot[botdasala]['comecou'] == 'sim':
                            pass
                    elif bot[botdasala]['chatipo'] == 'playersnaoforamparaolobby':
                        deletar = await self.deletarlobby(lobby=lobbyslug, liga=ligaslug)
                        mensagem = bot[botdasala]['conteudo']
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'comecarchat',
                                'mensagem': 'playersnaoforamparaolobby',
                                'botname': botname,
                                'conteudo': mensagem,
                        
                            }
                        )

                    elif bot[botdasala]['chatipo'] == 'radganhou':
                        pegadirplayers = await self.getdireplayers(liga=ligaslug, lobby=lobbyslug)
                        for x in range(0,len(pegadirplayers)):
                            player_dir = pegadirplayers[x].steamid.steamid
                           
                            add_points = await self.rempointslobby(liga =ligaslug, user = player_dir)

                        pegaradplayers = await self.getradplayers(liga=ligaslug, lobby=lobbyslug)
                        pegarligaplayers = await self.getligaplayers(liga=ligaslug)
                        for x in range(0,len(pegaradplayers)):
                            player_rad = pegaradplayers[x].steamid.steamid
                            
                            add_points = await self.addpointslobby(liga =ligaslug, user = player_rad)

                        mensagem = bot[botdasala]['conteudo']
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'comecarchat',
                                'mensagem': 'radganhou',
                                'botname': botname,
                                'conteudo': mensagem,
                        
                            }
                        )

                    elif bot[botdasala]['chatipo'] == 'dirganhou':
                        pegaradplayers = await self.getradplayers(liga=ligaslug, lobby=lobbyslug)
                        for x in range(0,len(pegaradplayers)):
                            player_rad = pegaradplayers[x].steamid.steamid
                            
                            add_points = await self.rempointslobby(liga =ligaslug, user = player_rad)

                        pegadirplayers = await self.getdireplayers(liga=ligaslug, lobby=lobbyslug)
                        pegarligaplayers = await self.getligaplayers(liga=ligaslug)
                        for x in range(0,len(pegadirplayers)):
                            player_dir = pegadirplayers[x].steamid.steamid
                            
                            add_points = await self.addpointslobby(liga =ligaslug, user = player_dir)
                        

                        mensagem = bot[botdasala]['conteudo']
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'comecarchat',
                                'mensagem': 'dirganhou',
                                'botname': botname,
                                'conteudo': mensagem,
                        
                            }
                        )
                    elif bot[botdasala]['chatipo'] == 'tirarpontosplayer':
                        playertirar = bot[botdasala]['conteudo']
                        tirarpontospl = await self.tirarpontosplayer(liga=ligaslug, lobby=lobbyslug, player=playertirar)
                    elif bot[botdasala]['chatipo'] == 'banirplayerdapla':
                        playerbanir = bot[botdasala]['conteudo']
                        banirplayer = await self.banirplayer(player=playerbanir)
                        #enviar mensagem dps
            else:
                pass


        elif tipodemensagem == 'comecarpartida':
            uuserr = data['userid']
            #username = data['user_chat']
            lobbyslug = data['lobbyslug']
            #msgplayer = data['msgplayer']
            ligaslug = data['liganame']
            botname = '<Dolex>'
            lobbystatus = await self.getlobbystatus(liga=ligaslug, lobby=lobbyslug)
            if lobbystatus is False:
                verificaseplayereocriador = await self.verificacriadordolobby(liga=ligaslug, lobby=lobbyslug, usuario=uuserr)
                if verificaseplayereocriador is True:
                    quantplayers = await self.pegarquantidadedeplayersnalobby(lobby=lobbyslug, liga=ligaslug)
                    if quantplayers == 10: # COLOCA '== 10' QUANDO TERMINAR DE TESTAR! 
                        #----------------------------------BOT COMEÇA AQUI---------------------------------------#

                        #PEGA NOME DA LOBBY
                        nomedalobby = await self.getnomedalobby(liga=ligaslug, lobby=lobbyslug)
                        player = await self.getlobbyplayers(lobby=lobbyslug, liga=ligaslug) #players[0].steamid.steamid
                        players = {
                            'player1': player[0].steamid.steamid,
                            'player1t': player[0].time,
                            'player2': player[1].steamid.steamid,
                            'player2t': player[1].time,
                            'player3': player[2].steamid.steamid,
                            'player3t': player[2].time,
                            'player4': player[3].steamid.steamid,
                            'player4t': player[3].time,
                            'player5': player[4].steamid.steamid,
                            'player5t': player[4].time,
                            'player6': player[5].steamid.steamid,
                            'player6t': player[5].time,
                            'player7': player[6].steamid.steamid,
                            'player7t': player[6].time,
                            'player8': player[7].steamid.steamid,
                            'player8t': player[7].time,
                            'player9': player[8].steamid.steamid,
                            'player9t': player[8].time,
                            'player10': player[9].steamid.steamid,
                            'player10t': player[9].time,
                        }  # players do lobby
                        
                        
                        bots = ConfigParser()
                        

                        #-> Mudar diretorio aqui se necessário
                        directoryfiles = '/home/dolexadmin/dolex/paginas/'
                        
                        paginaspath = os.path.dirname(os.path.abspath(__file__))
                        botspath = os.path.join(paginaspath, 'bots.ini')
                        bot_path = os.path.join(paginaspath, 'dolexbot.py')
                        bots.read(botspath)
                        nbots = len(bots.sections())

                        print('Numero de bots disponiveis: '+str(nbots))

                        bot = None
                        bot_sec = None

                        
                        #->Verifica se tem bot disponivel...
                        for i in range(nbots):
                            i += 1
                            if bots['BOT'+str(i)]['estado'] == 'livre':
                                bot = bots['BOT'+str(i)]
                                bot_sec = 'BOT'+str(i)
                                break
                            elif bots['BOT'+str(i)]['estado'] == 'ocupado':
                                continue
                            elif i == nbots and bots['BOT'+str(i)]['estado'] == 'ocupado':
                                bot = None
                        
                        if bot is not None:
                            ativarlobby = await self.ativarlobby(liga=ligaslug, lobby=lobbyslug)
                            cadastrarbotnalobby = await self.cadastrarbotnalobby(liga=ligaslug, lobby=lobbyslug, bot=bot_sec)
                            user = bot['usuario']
                            bpass = bot['senha'] 
                            bots[bot_sec]['estado'] = 'ocupado'
                            with open(botspath, 'w') as configfile:
                                bots.write(configfile)
                            # coloca '&'
                            #                                                PLAYERS:                       1     2     3     4     5     6     7     8     9     10
                            #---------------------------CHAMA O BOT EM SI AQUI------------------------------#-----#-----#-----#-----#-----#-----#-----#-----#-----#
                            #os.system("xfce4-terminal -x python3 "+directoryfiles+"dolexbot.py %s %s %s %s %s %s %s %s &" % (user, bpass, bot_sec, nomedalobby, players['player1'], players['player1t'], players['player2'], players['player2t']))
                            os.system("xfce4-terminal -x python3 "+directoryfiles+"dolexbot.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s &" % (user, bpass, bot_sec, nomedalobby, players['player1'], players['player1t'], players['player2'], players['player2t'], players['player3'], players['player3t'], players['player4'], players['player4t'], players['player5'], players['player5t'], players['player6'], players['player6t'], players['player7'], players['player7t'], players['player8'], players['player8t'], players['player9'], players['player9t'], players['player10'], players['player10t']))
                            
                            
                            await self.channel_layer.group_send(
                                self.lobbynome,
                                {
                                    'type': 'comecarchat',
                                    'mensagem': 'partidaceminstantes',
                                    'botname': botname,
                                    'conteudo': 'A partida começará em instantes...(Este processo pode levar alguns segundos)',
                                    
                            
                                }
                            )

                            
                            #------------------------------------------------------------
                        

                        else:
                            await self.channel_layer.group_send(
                                self.lobbynome,
                                {
                                    'type': 'comecarchat',
                                    'mensagem': 'sembotsparajogo',
                                    'botname': botname,
                                    'conteudo': 'Todos os bots estão ocupados no momento.',

                                }
                            )
                            
                        

                        #<- começar codigos nesse hash!

                        #----------------------------------BOT TERMINA AQUI---------------------------------------#
                    else:
                        await self.channel_layer.group_send(
                            self.lobbynome,
                            {
                                'type': 'comecarchat',
                                'mensagem': 'semjogsufi',
                                'botname': botname,
                                'conteudo': 'Sem jogadores suficiente.',

                            }
                        )
                else:
                    await self.channel_layer.group_send(
                        self.lobbynome,
                        {
                            'type': 'comecarchat',
                            'mensagem': 'naoedonoparacomecar',
                            'botname': botname,
                            'conteudo': 'Apenas o dono da lobby pode começar a partida.',

                        }
                    )
            else:
                await self.channel_layer.group_send(
                    self.lobbynome,
                    {
                        'type': 'comecarchat',
                        'mensagem': 'partidajacriada',
                        'botname': botname,
                        'conteudo': 'O bot já está criando a partida.',

                    }
                )
                



        # colocar outra if aqui!

#----------------------------------------------- MESSAGE TYPES --------------------------------------------------
    async def comecarchat(self, event):
        mensagem = event['mensagem']

        if mensagem == 'naopodetrocarslot':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'naopodetrocarslot': 'naopodetrocarslot',
                'botname': botname,
                'conteudo': conteudo,
            }))
        if mensagem == 'partidajacriada':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'partidajacriada': 'partidajacriada',
                'botname': botname,
                'conteudo': conteudo,
            }))
        ###########################
        if mensagem == 'partidaceminstantes':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'partidaceminstantes': 'partidaceminstantes',
                'botname': botname,
                'conteudo': conteudo,
            }))
        ###########################

        if mensagem == 'dirganhou':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'radganhou': 'radganhou',
                'botname': botname,
                'conteudo': conteudo,
            }))

        if mensagem == 'radganhou':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'radganhou': 'radganhou',
                'botname': botname,
                'conteudo': conteudo,
            }))
 
        if mensagem == 'playersnaoforamparaolobby':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'playersnaoforamparaolobby': 'playersnaoforamparaolobby',
                'botname': botname,
                'conteudo': conteudo,
            }))

        if mensagem == 'lobbycriadonodota':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'lobbycriadonodota': 'lobbycriadonodota',
                'botname': botname,
                'conteudo': conteudo,
            }))
       
        if mensagem == 'sembotsparajogo':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'sembotsparajogo': 'sembotsparajogo',
                'botname': botname,
                'conteudo': conteudo,
            }))
        if mensagem == 'naoedonoparacomecar':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'naoedono': 'naoedono',
                'botname': botname,
                'conteudo': conteudo,
            }))

        elif mensagem == 'semjogsufi':
            botname = event['botname']
            conteudo = event['conteudo']
            await self.send(text_data = json.dumps({
                'naohaplayers': 'naohaplayers',
                'botname': botname,
                'conteudo': conteudo,
            }))


    async def attlobby(self, event):
        mensagem = event['mensagem']
        ultposi = event['ultposi']

        await self.send(text_data = json.dumps({
            'apagoulobby': mensagem,
            'ultposi': ultposi,
        }))

    async def chatmessage(self, event):
        mensagem = event['mensagem']
        _user = event['user']

        await self.send(text_data = json.dumps({
            'mensagemchat': mensagem,
            'user': _user,
        }))

    async def attslot(self, event):
        mensagem = event['mensagem']

        if mensagem == 'playerquitou':
            ultposi = event['ultposi']
            await self.send(text_data = json.dumps({
                'excluirposi': 'sim',
                'ultposi':ultposi
            }))

        if mensagem == 'ocuparslot10':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '10',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '10',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot9':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '9',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '9',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot8':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '8',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '8',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot7':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '7',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '7',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot6':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '6',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '6',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot5':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '5',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '5',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot2':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '2',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '2',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot3':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '3',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '3',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot1':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '1',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '1',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))

        if mensagem == 'ocuparslot4':
            try:
                lob = event['lobant']
            except:
                lob = None
            if lob is not None:
                #print('hey') 
                _lobant = event['lobant']
                _usuario = event['user']
                _usuario_avatar = event['avatar']

                await self.send(text_data = json.dumps({
                    'ocuparlote': '4',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar,
                    'lobant': _lobant
                }))
            else:
                _usuario = event['user']
                _usuario_avatar = event['avatar']
                await self.send(text_data = json.dumps({
                    'ocuparlote': '4',
                    'user': _usuario,
                    'user_avatar': _usuario_avatar
                }))


    async def mcriou_lobby(self, event):
        mensagem = event['mensagem']
        if mensagem == 'crioulobby':

            await self.send(text_data = json.dumps({
                'crioulobby': 'sim'
            }))
        elif mensagem == 'naocrioulobby':
            await self.send(text_data = json.dumps({
                'crioulobby': 'nao'
            }))

        

    # AQUI FICA AS FUNÇÕES P/ CONEXÇÃO COM BANCO DE DADOS.
    @database_sync_to_async
    def banirplayer(self, player):
        _user = steamuser.objects.get(steamid=player)
        _user.banido = True
        _user.save()
    @database_sync_to_async
    def tirarpontosplayer(self, liga, lobby, player):
        _user = steamuser.objects.get(steamid=player)
        lig = ligas.objects.get(slug=liga)
        pl = lig.players_liga_set.get(steamid=_user)
        pl.pontos -= 150
        pl.save()

    @database_sync_to_async
    def rempointslobby(self, liga, user):
        
        _user = steamuser.objects.get(steamid=user)
        lig = ligas.objects.get(slug=liga)
        pl = lig.players_liga_set.get(steamid=_user)
        pl.pontos -= 50
        pl.save()

    @database_sync_to_async
    def addpointslobby(self, liga, user):
        
        _user = steamuser.objects.get(steamid=user)
        lig = ligas.objects.get(slug=liga)
        pl = lig.players_liga_set.get(steamid=_user)
        pl.pontos += 50
        pl.save()



    @database_sync_to_async
    def getdireplayers(self, liga, lobby):
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        dirplayers = lob.players_lobby_set.filter(time='dir')
        return dirplayers

    @database_sync_to_async
    def getradplayers(self, liga, lobby):
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        radplayers = lob.players_lobby_set.filter(time='rad')
        return radplayers

    @database_sync_to_async
    def getligaplayers(self, liga):
        lig = ligas.objects.get(slug=liga)
        playersliga = lig.players_liga_set.all()
        return playersliga

    @database_sync_to_async
    def getlobbystatus(self, liga, lobby):
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        return loby.ativo

    @database_sync_to_async
    def ativarlobby(self, liga, lobby):
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        loby.ativo = True
        loby.save()


    @database_sync_to_async
    def getbotdasala(self, liga, lobby):
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        try:
            bot = loby.bot
        except:
            bot = None
        return bot

    @database_sync_to_async
    def cadastrarbotnalobby(self, liga, lobby, bot):
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        loby.bot = bot
        loby.save()

    @database_sync_to_async
    def getnomedalobby(self, liga, lobby):
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        return lob.nome

    @database_sync_to_async
    def pegarquantidadedeplayersnalobby(self, lobby, liga):
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        lob = len(loby.players_lobby_set.all())
        return lob


    @database_sync_to_async
    def pegarslotantigo(self, user, lobby, liga):
        _user = steamuser.objects.get(steamid=user)
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        lob =  loby.players_lobby_set.get(steamid=_user)
        slot = lob.slot
        return slot

       
    @database_sync_to_async
    def verificarslot(self, liga, lobby, slot):
        ocupado = False
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        try:
            pp = lob.players_lobby_set.get(slot=slot)
            if pp:
                ocupado = True
        except players_lobby.DoesNotExist:
            ocupado = False
        return ocupado


    @database_sync_to_async
    def getlobby(self, lobby, liga):
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        return loby

    @database_sync_to_async
    def getlobbyplayers(self, lobby, liga):
        lig = ligas.objects.get(slug=liga)
        loby = lig.liga_lobby_set.get(slug=lobby)
        pls = loby.players_lobby_set.all()
        return pls

    @database_sync_to_async
    def verificasejogadorcriouliga(self, usuario, liga, lobby):
        criou = False
        user = steamuser.objects.get(steamid=usuario)
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        try:
            userlob = lob.players_lobby_set.get(steamid=user)
            if userlob:
                if userlob.slot == '1' and userlob.time == 'rad':
                    criou = True
                else:
                    criou = False
        except players_lobby.DoesNotExist:
            criou = False
        
        else:
            pass
        return criou
    
    #Verifica se o lobby esta vazio dps q a conexção do player com o lobby acaba
    @database_sync_to_async
    def verificacriadordolobby(self, liga, lobby, usuario):
        criador = True
        usr = steamuser.objects.get(steamid=usuario)
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        criador = lob.lobbycriador.nome
        user = usr.nome
        if criador == user:
            criador = True
        else:
            criador = False
        return criador

    @database_sync_to_async
    def verificalobbyvazio(self, lobby, liga):
        vazio = True
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        lobb = len(lob.players_lobby_set.all())
        if lobb is 0:
            vazio = True
        else:
            vazio = False
        return vazio

    #DELETA O LOBBY
    @database_sync_to_async
    def deletarlobby(self, lobby, liga):
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        lob.delete()
    #DELETALOBBYPLAYERQUANDOELESAI
    @database_sync_to_async
    def deletajogadordalobby(self, user, lobby, liga):
        lig = ligas.objects.get(slug=liga)
        lob = lig.liga_lobby_set.get(slug=lobby)
        user = steamuser.objects.get(steamid=user)
        userdalobby = lob.players_lobby_set.get(steamid=user)
        userdalobby.delete()

    @database_sync_to_async
    def getuserdata(self, user):
        _user = steamuser.objects.get(steamid=user)
        return _user
       
    @database_sync_to_async
    def verificasejogadorecadastrado(self, usuario, liga, lobby):
        cadastrado = False
        user = steamuser.objects.get(steamid=usuario)
        _liga = ligas.objects.get(slug=liga)
        lob = _liga.liga_lobby_set.get(slug=lobby)
        try:
            verifica = lob.players_lobby_set.get(steamid=user)
            if verifica:
                cadastrado = True
        except players_lobby.DoesNotExist:
            cadastrado = False

        return cadastrado

    @database_sync_to_async
    def cadastrarjogadornalobby(self, time, slot, usuario, liga, lobby):
        cadastrei = True
        user = steamuser.objects.get(steamid=usuario)
        _liga = ligas.objects.get(slug=liga)
        lob = _liga.liga_lobby_set.get(slug=lobby)
        cadpl = players_lobby(time=time, lobby=lob, steamid=user, slot=slot) 
        if cadpl.save():
            cadastrei = True
        else:
            cadastrei = False
        return cadastrei

    @database_sync_to_async
    def atualizarslotlobbyplayer(self, user, liga, lobby, slot):
        atualizei = True
        user = steamuser.objects.get(steamid=user)
        _liga = ligas.objects.get(slug=liga)
        lob = _liga.liga_lobby_set.get(slug=lobby)
        lobb = lob.players_lobby_set.get(steamid=user)
        lobb.slot = slot
        lobb.save()
        if slot <= 5:
            lobb.time = 'rad'
            lobb.save()
        elif slot >= 6:
            lobb.time = 'dir'
            lobb.save()
        
    



#--------------------------------------------------------------------------------------------







class LobbysConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ligaName = self.scope['url_route']['kwargs']['ligaName']
        self.lobbys_liga_group = 'lobbys_%s' % self.ligaName

        await self.channel_layer.group_add(
            self.lobbys_liga_group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.lobbys_liga_group,
            self.channel_name
        )

    async def receive(self, text_data):
        jtext_data = json.loads(text_data)
        message = jtext_data['message']
        liga = jtext_data['liga']
        if message == 'refresh':
            lobbys = await self.get_lobby_liga(liga)
            _lobbysc = len(lobbys)
            #print(lobbys)
            await self.channel_layer.group_send(
                self.lobbys_liga_group,
                {
                    'type': 'liga_refresh_message',
                    '_lobbysc': len(lobbys),
                    
                }
            )

    @database_sync_to_async
    def get_lobby_liga(self, liga):
        return ligas.objects.get(slug=liga).liga_lobby_set.all()

    # Receive message from room group
    async def liga_refresh_message(self, event):
        hm1 = event['_lobbysc']

        # Send message to WebSocket
        await self.send(text_data = json.dumps({
            '_lobbysc': hm1
        }))



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_session = 'lol'
        self.home_chat = 'home'

        # Join room group
        await self.channel_layer.group_add(
            self.home_chat,
            self.channel_name,
        )
        await self.accept()


    
    async def disconnect(self, close_code):
        #Leave room group
        await self.channel_layer.group_discard(
            self.home_chat,
            self.channel_name
        )
    
    #   Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        # Send message to room group
        await self.channel_layer.group_send(
            self.home_chat,
            {
                'type': 'chat_message',
                'user': user,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        user = event['user']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data = json.dumps({
            'user': user,
            'message': message
        }))
