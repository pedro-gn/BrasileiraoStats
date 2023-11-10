import csv
import random
from main.models import Jogador, Time
from datetime import datetime

# Abra o arquivo CSV e leia seus dados
with open('jogadores.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    data_nascimento_str = "1990-01-01"  # Substitua com a string da data desejada
    data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
    
    for row in reader:
        # Crie uma instância do modelo Time com base nos dados do CSV
        time = Jogador(
            nome=row['Nome'],
            time =Time.objects.get(nome='Atlético Mineiro-MG'),
            apelido =row['Apelido'],
            cartoes_v = random.randint(1, 5),
            cartoes_a = random.randint(1, 5),
            pe = "direito",
            n_camisa = 12,
            data_nascimento = data_nascimento,
            altura = 1.8,
            posicao = "atacante"
        )

        time.save()