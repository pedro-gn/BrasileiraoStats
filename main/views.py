from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Time, Jogador, Gol, Partida, Substituicao, JogadorPartida
from django.db.models import Count, F, ExpressionWrapper, IntegerField, Q, Avg, fields, Sum
from datetime import date
from .forms import JogadorSearchForm

def home(request):
    times = Time.objects.annotate(
    calculated_pontuacao = ExpressionWrapper(3 * F('vitorias') + F('empates'), output_field=IntegerField())).order_by('-calculated_pontuacao')
    
    # Query que retorna a contagem de gols de cada jogador
    jogadores_com_gols = Jogador.objects.select_related('time').annotate(num_gols=Count('gols_feitos')).order_by('-num_gols')[:5]
    
    ultimas_partidas = Partida.objects.select_related('time_mandante', 'time_visitante').order_by('-data')[:5]

    context = {
        "campeonato_selecionado": "Brasileirão 2022",
        "times": times,
        "jogadores_com_gols": jogadores_com_gols,
        "ultimas_partidas" : ultimas_partidas
    }

    return render(request, "home.html", context)

def partidas(request):
    partidas  = Partida.objects.all()
    context = {
        "partidas" : partidas,
    }
    return render(request, "pagina_partidas.html", context)
    
def partida(request, partida_id):
    partida = get_object_or_404(Partida, pk=partida_id)
    
    gols = Gol.objects.filter(partida_id=partida_id)
    
    
    context = {
        "gols" : gols,
        "partida" : partida,
        "time_mandante" : partida.time_mandante,
        "time_visitante" : partida.time_visitante
    }
    return render(request, "partida.html", context)

def jogadores(request):
    todos_jogadores = Jogador.objects.all()
    
    # Inicializar um novo formulário sem dados se a solicitação não contiver parâmetros de pesquisa
    form = JogadorSearchForm(request.GET) 
    if form.is_valid():
        query = form.cleaned_data['query']
        todos_jogadores = todos_jogadores.filter(nome__icontains=query)
        
    # Paginator dos jogadores
    jogadores_por_pagina = 20
    paginator = Paginator(todos_jogadores, jogadores_por_pagina)
    pagina_atual = request.GET.get('pagina_atual', 1)
    
    try:
        # Obtem a pagina especifica
        jogadores = paginator.page(pagina_atual)
    except PageNotAnInteger:
        # Se a pagina nao for um inteiro, mostra a primeira pagina
        jogadores = paginator.page(1)
    except EmptyPage:
        # Se a pagina for maior que o numero total de paginas, mostra a ultima pagina
        jogadores = paginator.page(paginator.num_pages)
    
    
    context = {
        "jogadores" : jogadores,
        'form': form
    }
    
    return render(request, 'pagina_jogadores.html', context)


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
    
    
    total_passes = JogadorPartida.objects.filter(jogador=jogador).aggregate(Sum('passes'))['passes__sum'] or 0
    total_finalizacoes = JogadorPartida.objects.filter(jogador=jogador).aggregate(Sum('finalizacoes'))['finalizacoes__sum'] or 0
    total_faltas = JogadorPartida.objects.filter(jogador=jogador).aggregate(Sum('faltas_cometidas'))['faltas_cometidas__sum'] or 0
    total_assistencias = JogadorPartida.objects.filter(jogador=jogador).aggregate(Sum('assistencias'))['assistencias__sum'] or 0
    
    context = {
        "total_faltas" : total_faltas,
        "total_assistencias" : total_assistencias,
        "total_finalizacoes" : total_finalizacoes,
        "total_passes" : total_passes,
        "time" : time,
        "ultimas_partidas" : ultimas_partidas,
        "numero_de_partidas" : numero_de_partidas,
        "jogador": jogador,
        "idade_anos" : idade_anos
    }
    return render(request, 'jogador.html', context)