import os

class Processo:
    def __init__(self, pid, tempo_chegada, tempo_execucao, prioridade):
        self.pid = pid
        self.tempo_chegada = tempo_chegada
        self.tempo_execucao = tempo_execucao
        self.prioridade = prioridade
        self.tempo_espera = 0
        self.tempo_retorno = 0

class EscalonadorPrioridadeMultiplasFilas:
    def __init__(self):
        self.filas = {}

    def adicionar_processo(self, processo):
        if processo.prioridade not in self.filas:
            self.filas[processo.prioridade] = []
        self.filas[processo.prioridade].append(processo)

    def executar(self):
        prioridades_ordenadas = sorted(self.filas.keys())
        tempo_atual = 0
        ordem_execucao = []

        for prioridade in prioridades_ordenadas:
            fila = self.filas[prioridade]

            for processo in sorted(fila, key=lambda p: p.tempo_chegada):
                if tempo_atual < processo.tempo_chegada:
                    tempo_atual = processo.tempo_chegada
                processo.tempo_espera = tempo_atual - processo.tempo_chegada
                processo.tempo_retorno = processo.tempo_espera + processo.tempo_execucao
                tempo_atual += processo.tempo_execucao
                ordem_execucao.append(processo)

        return ordem_execucao

    @staticmethod
    def calcular_medias(processos):
        total_tempo_espera = sum(p.tempo_espera for p in processos)
        total_tempo_retorno = sum(p.tempo_retorno for p in processos)
        n = len(processos)
        return total_tempo_espera / n, total_tempo_retorno / n

    @staticmethod
    def escrever_saida(ordem_execucao, media_tempo_espera, media_tempo_retorno, nome_arquivo):
        with open(nome_arquivo, 'a', encoding='utf-8') as arquivo:
            arquivo.write("--------------------------------\n")
            arquivo.write("Caua Cristian -> Priority Scheduling Multiple Queues\n\n")
            arquivo.write("Ordem de Execução: " + " → ".join(p.pid for p in ordem_execucao) + "\n\n")
            arquivo.write("Processo | Tempo de Chegada | Tempo de Execução | Prioridade | Tempo de Espera | Tempo de Retorno\n")
            for processo in ordem_execucao:
                arquivo.write(f"{processo.pid}       | {processo.tempo_chegada}                | {processo.tempo_execucao}                 | {processo.prioridade}          | {processo.tempo_espera}               | {processo.tempo_retorno}\n")
            arquivo.write(f"\nTempo Médio de Espera: {media_tempo_espera:.2f}\n")
            arquivo.write(f"Tempo Médio de Retorno: {media_tempo_retorno:.2f}\n")
            arquivo.write("--------------------------------\n\n")

if __name__ == "__main__":
    escalonador = EscalonadorPrioridadeMultiplasFilas()

    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    nome_arquivo_entrada = os.path.join(pasta_atual, "..", "Entrada.txt")
    nome_arquivo_saida = os.path.join(pasta_atual, "..", "Resultados.txt")

    with open(nome_arquivo_entrada, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas[1:]:
            partes = linha.split()
            pid = partes[0]
            tempo_chegada = int(partes[1])
            tempo_execucao = int(partes[2])
            prioridade = int(partes[3])
            escalonador.adicionar_processo(Processo(pid, tempo_chegada, tempo_execucao, prioridade))

    ordem_execucao = escalonador.executar()

    media_tempo_espera, media_tempo_retorno = escalonador.calcular_medias(ordem_execucao)

    escalonador.escrever_saida(ordem_execucao, media_tempo_espera, media_tempo_retorno, nome_arquivo_saida)