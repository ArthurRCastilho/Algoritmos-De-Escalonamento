class Processo:
    def __init__(self, id, chegada, execucao, prioridade):
        self.id = id
        self.chegada = chegada
        self.execucao = execucao
        self.prioridade = prioridade
        self.espera = 0
        self.retorno = 0

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

def escalonamento_fcfs(processos):
    processos.sort(key=lambda p: p.chegada)

    tempo_atual = 0
    tempos_espera = []
    tempos_retorno = []

    for processo in processos:
        if tempo_atual < processo.chegada:
            tempo_atual = processo.chegada

        processo.espera = tempo_atual - processo.chegada

        processo.retorno = processo.espera + processo.execucao

        tempo_atual += processo.execucao

        tempos_espera.append(processo.espera)
        tempos_retorno.append(processo.retorno)

    media_espera = sum(tempos_espera) / len(processos)
    media_retorno = sum(tempos_retorno) / len(processos)

    print("\nOrdem de Execução:", " → ".join([p.id for p in processos]))
    print("\nProcesso | Tempo de Chegada | Tempo de Execução | Prioridade | Tempo de Espera | Tempo de Retorno")
    for p in processos:
        print(f"{p.id:<8} | {p.chegada:<16} | {p.execucao:<17} | {p.prioridade:<10} | {p.espera:<15} | {p.retorno:<15}")
    print(f"\nTempo Médio de Espera: {media_espera:.2f}")
    print(f"Tempo Médio de Retorno: {media_retorno:.2f}")

    with open("Resultados.txt", "w") as arquivo:
        arquivo.write("FCFS - First Come, First Served\n")
        arquivo.write("Ordem de Execução: " + " → ".join([p.id for p in processos]) + "\n\n")
        arquivo.write("Processo | Tempo de Chegada | Tempo de Execução | Prioridade | Tempo de Espera | Tempo de Retorno\n")
        for p in processos:
            arquivo.write(f"{p.id:<8} | {p.chegada:<16} | {p.execucao:<17} | {p.prioridade:<10} | {p.espera:<15} | {p.retorno:<15}\n")
        arquivo.write(f"\nTempo Médio de Espera: {media_espera:.2f}\n")
        arquivo.write(f"Tempo Médio de Retorno: {media_retorno:.2f}\n")

processos = ler_processos_arquivo("Entrada.txt")

escalonamento_fcfs(processos)
