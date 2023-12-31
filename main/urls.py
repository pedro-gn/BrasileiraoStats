from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("times", views.times, name="times"),
    path("jogadores", views.jogadores, name="jogadores"),
    path("partidas", views.partidas, name="partidas"),
    path('times/<str:nome_time>/', views.time_detail, name='time_detail'),
    path('jogadores/<int:jogador_id>/', views.jogador_detail, name='jogador_detail'),
    path('partidas/<int:partida_id>/', views.partida, name='partida')
]