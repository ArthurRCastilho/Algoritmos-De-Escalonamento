class Processo:
    def __init__(self, id, chegada, execucao, prioridade):
        self.id = id
        self.chegada = chegada
        self.execucao = execucao
        self.prioridade = prioridade
        self.espera = 0
        self.retorno = 0
        self.tempo_restante = execucao

# Função para calcular tempos de espera e retorno usando Priority Scheduling (não-preemptivo)
def priority_scheduling_nao_preemptivo(processos):
    # Cria uma cópia da lista de processos para evitar modificações na original
    processos_copia = sorted(processos, key=lambda p: (p.chegada, p.prioridade))

    tempo_atual = 0
    ordem_execucao = []

    while processos_copia:
        # Seleciona os processos disponíveis (que já chegaram)
        disponiveis = [p for p in processos_copia if p.chegada <= tempo_atual]

        if not disponiveis:  # Se nenhum processo estiver disponível, avança o tempo
            tempo_atual += 1
            continue

        # Seleciona o processo de maior prioridade (menor valor de prioridade)
        processo_atual = min(disponiveis, key=lambda p: p.prioridade)
        processos_copia.remove(processo_atual)

        # Atualiza os tempos do processo selecionado
        ordem_execucao.append(processo_atual.id)
        processo_atual.espera = tempo_atual - processo_atual.chegada
        processo_atual.retorno = processo_atual.espera + processo_atual.execucao

        # Atualiza o tempo atual após a execução do processo
        tempo_atual += processo_atual.execucao

    return ordem_execucao

# Função para calcular os tempos médios
def calcular_tempos_medios(processos):
    if not processos:
        return 0, 0  # Evita divisão por zero
    tempo_medio_espera = sum(p.espera for p in processos) / len(processos)
    tempo_medio_retorno = sum(p.retorno for p in processos) / len(processos)
    return tempo_medio_espera, tempo_medio_retorno

# Função para salvar os resultados em um arquivo
def salvar_resultados(resultados, nome_arquivo="Resultados.txt"):
    with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write("--------------------------------\n")
        arquivo.write("Gabriel Cândido -> Priority Scheduling\n")
        arquivo.write("\nOrdem de Execução: " + " → ".join(resultados["ordem_execucao"]) + "\n\n")
        arquivo.write(f"{'Processo':<10}{'Tempo de Chegada':<20}{'Tempo de Execução':<20}{'Prioridade':<20}{'Tempo de Espera':<20}{'Tempo de Retorno':<20}\n")
        
        for processo in resultados["processos"]:
            arquivo.write(f"{processo.id:<10}{processo.chegada:<20}{processo.execucao:<20}{processo.prioridade:<20}{processo.espera:<20}{processo.retorno:<20}\n")
        
        arquivo.write(f"\nMédia de Espera: {resultados['media_espera']:.2f}\n")
        arquivo.write(f"Média de Retorno: {resultados['media_retorno']:.2f}\n")
        arquivo.write("--------------------------------\n\n")

# Função para exibir os resultados
def exibir_resultados(processos, ordem_execucao, tempo_medio_espera, tempo_medio_retorno):
    print("----------------------------------------------------")
    print("Gabriel Cândido -> Priority Scheduling")
    print("Ordem de Execução: " + " → ".join(ordem_execucao))
    print()
    print("Processo | Tempo de Chegada | Tempo de Execução | Prioridade | Tempo de Espera | Tempo de Retorno")
    for p in processos:
        print(f"{p.id:<8} | {p.chegada:<16} | {p.execucao:<16} | {p.prioridade:<9} | {p.espera:<14} | {p.retorno:<14}")
    print()
    print(f"Tempo Médio de Espera: {tempo_medio_espera:.2f}")
    print(f"Tempo Médio de Retorno: {tempo_medio_retorno:.2f}")
    print("----------------------------------------------------")

# Dados iniciais
processos = [
    Processo("P1", 0, 5, 2),
    Processo("P2", 2, 3, 1),
    Processo("P3", 4, 8, 3),
    Processo("P4", 5, 6, 2),
    Processo("P5", 11, 8, 1)
]

# Executa o algoritmo
ordem_execucao = priority_scheduling_nao_preemptivo(processos)

# Calcula os tempos médios
tempo_medio_espera, tempo_medio_retorno = calcular_tempos_medios(processos)

# Prepara os resultados para salvar
resultados = {
    "ordem_execucao": ordem_execucao,
    "processos": processos,
    "media_espera": tempo_medio_espera,
    "media_retorno": tempo_medio_retorno
}

# Salva os resultados em um arquivo
salvar_resultados(resultados)

# Exibe os resultados
exibir_resultados(processos, ordem_execucao, tempo_medio_espera, tempo_medio_retorno)
