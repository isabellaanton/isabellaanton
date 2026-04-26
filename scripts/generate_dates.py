import subprocess
import random
import os
from datetime import date, timedelta

# Configurações de Identidade
EMAIL = "isabellagaspar65@gmail.com"
NAME = "github-actions[bot]"

# Feriados nacionais brasileiros (fixos)
FERIADOS = {
    (1, 1), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (11, 20), (12, 25),
    (3, 28), (3, 29), (3, 30), (3, 3), (3, 4), (3, 5), # Datas móveis aproximadas
}

MESES_FRACOS = {1, 6, 12}

def deve_commitar(dia: date) -> bool:
    # 1. Ignora finais de semana (Sábado=5, Domingo=6)
    if dia.weekday() >= 5:
        return False
    
    # 2. Ignora feriados
    if (dia.month, dia.day) in FERIADOS:
        return False
    
    # 3. Lógica de Probabilidade para atingir ~180 dias/ano
    # Dias úteis totais no ano são aprox. 261.
    # 180 / 261 = ~68% de chance média.
    
    if dia.month in MESES_FRACOS:
        return random.random() < 0.35  # Menos atividade em meses de férias
    
    return random.random() < 0.72      # Compensação nos meses normais

def quantos_commits(dia: date) -> int:
    if dia.month in MESES_FRACOS:
        return random.randint(1, 2)
    return random.randint(1, 4)        # Variedade visual no gráfico

# Configuração inicial do Git
subprocess.run(["git", "config", "user.email", EMAIL], check=True)
subprocess.run(["git", "config", "user.name", NAME], check=True)

hoje = date.today()
inicio = hoje - timedelta(days=365)
total_commits = 0
dias_ativos = 0

dia_atual = inicio
while dia_atual <= hoje:
    if deve_commitar(dia_atual):
        dias_ativos += 1
        n = quantos_commits(dia_atual)
        
        for _ in range(n):
            # Horário aleatório para não parecer um bot (entre 09:00 e 20:00)
            hora = random.randint(9, 20)
            minuto = random.randint(10, 59)
            data_str = dia_atual.strftime(f"%Y-%m-%dT{hora}:{minuto}:00")
            
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = data_str
            env["GIT_COMMITTER_DATE"] = data_str
            
            subprocess.run([
                "git", "commit", "--allow-empty", 
                "-m", "chore: technical maintenance and updates", 
                "--date", data_str
            ], env=env, check=True, capture_output=True)
            
            total_commits += 1
            
    dia_atual += timedelta(days=1)

print(f"Processo concluído!")
print(f"Dias com atividade: {dias_ativos}")
print(f"Total de commits: {total_commits}")

# Push final
# subprocess.run(["git", "push"], check=True)
