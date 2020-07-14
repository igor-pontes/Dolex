from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='paginas-home'),
    path('sobre/', views.sobre, name='paginas-sobre'),
    path('login/', views.login, name='paginas-login'),
    path('process/', views.process_login, name='paginas-process'),
    path('logout/', views.logout, name='paginas-logout'),
    path('ligas/<int:start>/', views.pag_ligas, name='paginas-ligas'),
    path('ligas/', views.pag_ligas, name='paginas-ligas'),
    path('liga/<slug:liga>/', views.pag_liga, name='paginas-liga'),
    path('liga/', views.pag_liga, name='paginas-liga'),
    path('liga/<slug:liga>/ranking', views.pag_liga_ranking, name='paginas-liga-ranking'),
    path('liga/<slug:liga>/entrar', views.pag_liga_entrar, name='paginas-liga-entrar'),
    path('liga/<slug:liga>/sair', views.pag_liga_sair, name='paginas-liga-sair'),
    path('liga/<slug:liga>/lobby', views.pag_liga_lobby, name='paginas-liga-lobby'),
    path('liga/<slug:liga>/lobby/<slug:lobby>', views.pag_liga_lobby_page, name='paginas-liga-lobby-page'),
    path('liga/<slug:liga>/criarlobby', views.pag_criar_lobby, name='paginas-criar-lobby'),
    path('liga/<slug:liga>/lobby/<slug:lobby>/entrar', views.pag_liga_lobby_entrar, name='paginas-liga-lobby-entrar'),
]
