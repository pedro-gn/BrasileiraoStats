from django.contrib import admin
from .models import Time, Jogador, Gol, Partida, Substituicao, JogadorPartida


# Register your models here.
admin.site.register(Time)
admin.site.register(Jogador)
admin.site.register(Gol)
admin.site.register(Partida)
admin.site.register(JogadorPartida)
admin.site.register(Substituicao)