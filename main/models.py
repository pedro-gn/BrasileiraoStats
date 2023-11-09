from django.db import models

# Create your models here.

class Time(models.Model):
    nome = models.CharField(max_length=50, primary_key=True)
    tecnico = models.CharField(max_length=50)
    vitorias = models.IntegerField()
    derrotas = models.IntegerField()
    empates = models.IntegerField()
    gols_s = models.IntegerField()
    gols_m = models.IntegerField()
    estadio = models.CharField(max_length=50)
    escudo = models.CharField(max_length=255)
    sigla = models.CharField(max_length=10)
    
    #Atributos derivados
    @property
    def jogos(self):
        return self.vitorias + self.derrotas + self.empates
    
    @property
    def saldo_gols(self):
        return self.gols_m - self.gols_s
    
    @property
    def pontuacao(self):
        return self.vitorias * 3 + self.empates

    def __str__(self):
        return self.nome
    
    
class Jogador(models.Model):
    nome = models.CharField(max_length=50)
    apelido = models.CharField(max_length=50)
    posicao = models.CharField(max_length=50)
    n_camisa = models.IntegerField()
    cartoes_v = models.IntegerField()
    cartoes_a = models.IntegerField() 
    pe = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    altura = models.FloatField()
    foto = models.CharField(max_length=255, default='main/images/avatarjogador.png')
    
    time = models.ForeignKey(Time, on_delete=models.CASCADE)

class Partida(models.Model):
    time_mandante = models.ForeignKey(Time, related_name="partidas_mandante", on_delete=models.CASCADE)
    time_visitante = models.ForeignKey(Time, related_name="partidas_visitante", on_delete=models.CASCADE)
    gols_mandante= models.IntegerField()
    gols_visitante = models.IntegerField()
    
    data = models.DateTimeField()
    rodada =  models.IntegerField()
    
class Gol(models.Model):
    jogador_gol = models.ForeignKey(Jogador, related_name='gols_feitos', on_delete=models.CASCADE)
    jogador_ass = models.ForeignKey(Jogador, related_name='assistencias', on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    
class Substituicao(models.Model):
    jogador_saiu = models.ForeignKey(Jogador, related_name='substituicao_saiu', on_delete=models.CASCADE)
    jogador_entrou = models.ForeignKey(Jogador, related_name='substituicao_entrou', on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    
class JogadorPartida(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    
    cartoes_amarelos = models.IntegerField(default=0)
    cartoes_vermelhos = models.IntegerField(default=0)
    faltas_cometidas = models.IntegerField(default=0)
    assistencias = models.IntegerField(default=0)
    finalizacoes = models.IntegerField(default=0)
    passes = models.IntegerField(default=0)


    class Meta:
        unique_together = ['jogador', 'partida']


