from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url('ws/home/', consumers.ChatConsumer),
    url(r'^ws/liga/(?P<ligaName>[^/]+)/$', consumers.LobbysConsumer),
    url(r'^ws/liga/(?P<ligaName>[^/]+)/lobby/(?P<lobbyslug>[^/]+)/$', consumers.LobbyConsumer),
]