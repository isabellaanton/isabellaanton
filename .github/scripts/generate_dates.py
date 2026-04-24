import subprocess
import random
from datetime import date, timedelta

# Feriados nacionais brasileiros (fixos)
FERIADOS = {
    (1, 1), (4, 21), (5, 1), (9, 7),
    (10, 12), (11, 2), (11, 15), (11, 20), (12, 25),
    # Semana santa (aproximada)
    (3, 28), (3, 29), (3, 30),
    # Carnaval (aproximado)
    (3, 3), (3, 4), (3, 5),
}

# Meses com menos atividade
MESES_FRACOS = {1, 6, 12}  # janeiro, junho (festas), dezembro

def deve_commitar(dia: date) -> bool:
    # Sem fins de semana
    if dia.weekday() >= 5:
        return False
    # Sem feriados
    if (dia.month, dia.day) in FERIADOS:
        return False
    # Meses fracos: 40% de chance só
    if dia.month in MESES_FRACOS:
        return random.random() < 0.40
    # Dias normais: 85% de chance
    return random.random() < 0.85

def quantos_commits(dia: date) -> int:
    if dia.month in MESES_FRACOS:
        return random.randint(1, 2)
    return random.randint(1, 5)

# Gera os últimos 365 dias
hoje = date.today()
inicio = hoje - timedelta(days=365)

subprocess.run(["git", "config", "user.email", "isabellagaspar65@gmail.com"], check=True)
subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)

total = 0
dia = inicio
while dia <= hoje:
    if deve_commitar(dia):
        n = quantos_commits(dia)
        for _ in range(n):
            data_str = dia.strftime("%Y-%m-%dT12:00:00")
            env = {"GIT_AUTHOR_DATE": data_str, "GIT_COMMITTER_DATE": data_str}
            subprocess.run(["git", "commit", "--allow-empty",
                           "-m", "chore: update contribution graph",
                           "--date", data_str], env={**__import__('os').environ, **env}, check=True)
        total += n
    dia += timedelta(days=1)

print(f"Total de commits criados: {total}")
subprocess.run(["git", "push"], check=True)
