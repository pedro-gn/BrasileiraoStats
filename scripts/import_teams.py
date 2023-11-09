import csv
from main.models import Time

# Abra o arquivo CSV e leia seus dados
with open('teams.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        # Crie uma instância do modelo Time com base nos dados do CSV
        time = Time(
            nome=row['name'],
            tecnico=row['coachName'],
            vitorias=int(row['won']),
            derrotas=int(row['lost']),
            empates=int(row['draw']),
            gols_m=int(row['goalsFor']),
            gols_s=int(row['goalsAgainst']),
            estadio=row['venue'],
            escudo=row['crest'],
            sigla = row['tla']
        )

        time.save()
