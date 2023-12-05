import csv
import random
from main.models import Jogador, Time
from datetime import datetime

# Abra o arquivo CSV e leia seus dados
with open('csvs/jogadores.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    data_nascimento_str = "1990-01-01"  
    data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
    
    for row in reader:
        
        if row['Time'] == "Time nao encontrado":
            continue
        
        try:
            time_instance = Time.objects.get(nome=row['Time'])
        except Time.DoesNotExist:
            # Se o Time não existir, pule para a próxima iteração
            continue
        
        
        
        # Crie uma instância do modelo Time com base nos dados do CSV
        time = Jogador(
            nome=row['Nome'],
            time = time_instance,
            apelido =row['Apelido'],
            cartoes_v = random.randint(1, 5),
            cartoes_a = random.randint(1, 5),
            pe = "Direito",
            n_camisa = random.randint(1, 20),
            data_nascimento = data_nascimento,
            altura = 1.8,
            posicao = "Atacante"
        )

        time.save()