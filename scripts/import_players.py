import csv
import random
from main.models import Jogador

# Abra o arquivo CSV e leia seus dados
with open('jogadores.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        # Crie uma instância do modelo Time com base nos dados do CSV
        time = Jogador(
            nome=row['Nome'],
            time =row['Time'],
            apelido =row['Apelido'],
            cartoes_v = random.randint(1, 5),
            cartoes_a = random.randint(1, 5),
            pe = "direito"
            
        )

        time.save()