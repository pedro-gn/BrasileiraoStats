from django.shortcuts import render, get_object_or_404
from .models import Time, Jogador, Gol, Partida, Substituicao, JogadorPartida
from django.db.models import Count, F, ExpressionWrapper, IntegerField, Q, Avg, fields
from datetime import date

def home(request):
    times = Time.objects.annotate(
    calculated_pontuacao = ExpressionWrapper(3 * F('vitorias') + F('empates'), output_field=IntegerField())).order_by('-calculated_pontuacao')
    
    # Query que retorna a contagem de gols de cada jogador
    jogadores_com_gols = Jogador.objects.select_related('time').annotate(num_gols=Count('gols_feitos')).order_by('-num_gols')
    
    ultimas_partidas = Partida.objects.select_related('time_mandante', 'time_visitante').order_by('-data')[:5]

    context = {
        "campeonato_selecionado": "Brasileirão 2022",
        "times": times,
        "jogadores_com_gols": jogadores_com_gols,
        "ultimas_partidas" : ultimas_partidas
    }

    return render(request, "home.html", context)



def times(request):
    times = Time.objects.annotate(
    calculated_pontuacao = ExpressionWrapper(3 * F('vitorias') + F('empates'), output_field=IntegerField())).order_by('-calculated_pontuacao')
    
    
    context = {
        "times" : times    
    }
    return render(request, 'pagina_times.html', context)

def time_detail(request, nome_time):
    time = get_object_or_404(Time, nome=nome_time)
    
    #media de idade do time
    jogadores = Jogador.objects.filter(time_id=time.pk)
    
    if jogadores.exists():
        # Apenas calcule a média se houver jogadores
        media_idade = jogadores.annotate(
            idade=ExpressionWrapper(date.today() - F('data_nascimento'), output_field=fields.DurationField())
        ).aggregate(media_idade=Avg('idade'))

        media_idade_anos = round(media_idade['media_idade'].days / 365.25, 2)
    else:
        # Trate o caso em que não há jogadores cadastrados
        media_idade_anos = 0.0  # Ou qualquer outro valor padrão que você preferir
    
    
    #calculo do numero de partidas e de jogadores do time especifico
    numero_de_jogadores = time.jogador_set.count()
    numero_de_partidas = time.partidas_mandante.count() + time.partidas_visitante.count()
    
    #ultimas partidas
    partidas = Partida.objects.filter(Q(time_mandante_id=time.pk) | Q(time_visitante_id=time.pk))
    ultimas_partidas = partidas.order_by('-data')
    
    #jogadores do time
    jogadores = Jogador.objects.filter(time_id=time.pk)
    
    context = {
        "media_idade_anos" : media_idade_anos,
        "numero_de_partidas" : numero_de_partidas,
        "numero_de_jogadores" : numero_de_jogadores,
        "jogadores" : jogadores,
        "ultimas_partidas" : ultimas_partidas,
        'time': time
    }
    
    return render(request, 'time.html', context)


def jogador_detail(request, jogador_id):
    jogador = get_object_or_404(Jogador, pk=jogador_id)
    
    #idade do jogador em anos
    idade_anos = round((date.today() - jogador.data_nascimento).days / 365.25)
    
    #numero de partidas que o jogador jogou
    numero_de_partidas = JogadorPartida.objects.filter(jogador_id=jogador.pk).count()
    
    #time do jogador
    time = jogador.time
    
    #ultimas partidas do jogador
    ultimas_partidas = JogadorPartida.objects.select_related('partida__time_mandante', 'partida__time_visitante').filter(jogador=jogador.pk).order_by('-partida__data')[:5]
    
    context = {
        "time" : time,
        "ultimas_partidas" : ultimas_partidas,
        "numero_de_partidas" : numero_de_partidas,
        "jogador": jogador,
        "idade_anos" : idade_anos
    }
    return render(request, 'jogador.html', context)