import csv
from collections import deque

class Processo:
    def __init__(self, id, chegada, execucao, prioridade):
        self.id = id
        self.chegada = chegada
        self.execucao = execucao
        self.prioridade = prioridade
        self.espera = 0
        self.retorno = 0
        self.tempo_restante = execucao

def ler_processos_arquivo(nome_arquivo):
    processos = []
    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas[1:]:
            partes = linha.split()
            id = partes[0]
            chegada = int(partes[1])
            execucao = int(partes[2])
            prioridade = int(partes[3])
            processos.append(Processo(id, chegada, execucao, prioridade))
    return processos

def round_robin(processos, time_quantum):
    queue = deque()
    time = 0
    completed_processes = []
    execution_order = []

    while processos or queue:
        while processos and processos[0].chegada <= time:
            queue.append(processos.pop(0))

        if queue:
            current_process = queue.popleft()
            execution_order.append(current_process.id)
            exec_time = min(time_quantum, current_process.tempo_restante)
            current_process.tempo_restante -= exec_time
            time += exec_time

            while processos and processos[0].chegada <= time:
                queue.append(processos.pop(0))

            if current_process.tempo_restante > 0:
                queue.append(current_process)
            else:
                current_process.retorno = time - current_process.chegada
                completed_processes.append(current_process)

            for p in queue:
                p.espera += exec_time
        else:
            time += 1

    return completed_processes, execution_order

def calcular_tempos(processos):
    tempo_medio_espera = sum(p.espera for p in processos) / len(processos)
    tempo_medio_retorno = sum(p.retorno for p in processos) / len(processos)
    return tempo_medio_espera, tempo_medio_retorno

def salvar_resultados(processos, execution_order, tempo_medio_espera, tempo_medio_retorno, nome_arquivo):
    print("-------\nRound Robin (RR)\n\n")
    print("Ordem de Execução: " + " -> ".join(execution_order) + "\n\n")
    print(f"{'Processo':<10}{'Tempo de Espera':<20}{'Tempo de Retorno':<20}\n")
    for p in processos:
        print(f"{p.id:<10}{p.espera:<20}{p.retorno:<20}\n")
    print("\n")
    print(f"Tempo Médio de Espera: {tempo_medio_espera:.2f}\n")
    print(f"Tempo Médio de Retorno: {tempo_medio_retorno:.2f}\n")
    print("-------\n")

    # Salva os resultados
    with open(nome_arquivo, 'a') as file:  # 'a' para adicionar ao arquivo
        file.write("--------------------------------\nArthur Rodrigues -> Round Robin (RR)\n\n")
        file.write("Ordem de Execução: " + " -> ".join(execution_order) + "\n\n")
        file.write(f"{'Processo':<10}{'Tempo de Espera':<20}{'Tempo de Retorno':<20}\n")
        for p in processos:
            file.write(f"{p.id:<10}{p.espera:<20}{p.retorno:<20}\n")
        file.write("\n")
        file.write(f"Tempo Médio de Espera: {tempo_medio_espera:.2f}\n")
        file.write(f"Tempo Médio de Retorno: {tempo_medio_retorno:.2f}\n")
        file.write("--------------------------------\n")

# Configuração inicial
input_file = 'Entrada.txt'
output_file = 'Resultados.txt'
time_quantum = 2

# Leitura dos processos
todos_processos = ler_processos_arquivo(input_file)
todos_processos.sort(key=lambda p: p.chegada)

# Execução do Round Robin
processos_completos, execution_order = round_robin(todos_processos, time_quantum)

# Cálculo dos tempos
tempo_medio_espera, tempo_medio_retorno = calcular_tempos(processos_completos)

# Salvar resultados
salvar_resultados(processos_completos, execution_order, tempo_medio_espera, tempo_medio_retorno, output_file)
