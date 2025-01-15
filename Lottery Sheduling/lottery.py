import random

class Processo:
    def __init__(self, id, chegada, duracao, prioridade):
        self.id = id
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade
        self.espera = 0
        self.retorno = 0
        self.tempo_restante = duracao

def escalonamento_loteria(processos):
    tempo = 0
    processos_concluidos = []
    ordem_execucao = []
    total_espera = 0
    total_retorno = 0

    bilhetes = []
    for processo in processos:
        bilhetes.extend([processo.id] * processo.prioridade)

    while processos:
        bilhete_sorteado = random.choice(bilhetes)
        processo_escolhido = next(p for p in processos if p.id == bilhete_sorteado)

        tempo += 1
        processo_escolhido.tempo_restante -= 1
        ordem_execucao.append(processo_escolhido.id)

        if processo_escolhido.tempo_restante == 0:
            processo_escolhido.retorno = tempo - processo_escolhido.chegada
            processo_escolhido.espera = processo_escolhido.retorno - processo_escolhido.duracao
            processos_concluidos.append(processo_escolhido)
            processos.remove(processo_escolhido)
            bilhetes = [b for b in bilhetes if b != processo_escolhido.id]

    total_espera = sum(p.espera for p in processos_concluidos)
    total_retorno = sum(p.retorno for p in processos_concluidos)
    media_espera = total_espera / len(processos_concluidos)
    media_retorno = total_retorno / len(processos_concluidos)

    return processos_concluidos, ordem_execucao, media_espera, media_retorno

def salvar_resultados(resultados, nome_arquivo="Resultados.txt"):
    with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write("--------------------------------\n")
        arquivo.write("Rhennan Augusto -> Lottery Scheduling\n")
        arquivo.write("\nOrdem de Execução: " + " → ".join(resultados["ordem_execucao"]) + "\n\n")
        arquivo.write(f"{'Processo':<10}{'Tempo de Espera':<20}{'Tempo de Retorno':<20}\n")
        
        for processo in resultados["processos"]:
            arquivo.write(f"{processo.id:<10}{processo.espera:<20}{processo.retorno:<20}\n")
        
       
        arquivo.write(f"\nMédia de Espera: {resultados['media_espera']:.2f}\n")
        arquivo.write(f"Média de Retorno: {resultados['media_retorno']:.2f}\n")
        arquivo.write("--------------------------------\n\n")



lista_processos = [
    Processo("P1", 0, 5, 2),
    Processo("P2", 2, 3, 1),
    Processo("P3", 4, 8, 3),
    Processo("P4", 5, 6, 2),
    Processo("P5", 11, 8, 1),
]

concluidos, execucao, media_espera, media_retorno = escalonamento_loteria(lista_processos)

resultados_para_salvar = {
    "processos": concluidos,
    "ordem_execucao": execucao,
    "media_espera": media_espera,
    "media_retorno": media_retorno,
}

salvar_resultados(resultados_para_salvar)

print("Resultados salvos no arquivo 'Resultados.txt'.")
