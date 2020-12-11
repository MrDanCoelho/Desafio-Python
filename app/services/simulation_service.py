from app.domain.models.resultado_model import resultado_model
from app.domain.models.propriedade_model import propriedade_model
from app.domain.enums.enum_tipo_jogador import enum_tipo_jogador
from app.domain.models.jogador_model import jogador_model
import time
import random

class simulation_service:

    def jogador_impulsivo(self, jogador: jogador_model, propriedade: propriedade_model) -> None:
        """Comportamento de um jogador impulsivo dentro da simulação de Banco Imobiliário

        Args:
            jogador (jogador_model): o jogador que esta fazendo a ação
            propriedade (propriedade_model): a propriedade onde o jogador se encontra
        """
        if jogador.saldo >= propriedade.valor_compra:
            self.comprar_propriedade(jogador, propriedade)

    def jogador_exigente(self, jogador: jogador_model, propriedade: propriedade_model) -> None:
        """Comportamento de um jogador exigente dentro da simulação de Banco Imobiliário

        Args:
            jogador (jogador_model): o jogador que esta fazendo a ação
            propriedade (propriedade_model): a propriedade onde o jogador se encontra
        """
        if jogador.saldo >= propriedade.valor_compra and propriedade.valor_aluguel >= 50:
            self.comprar_propriedade(jogador, propriedade)

    def jogador_cauteloso(self, jogador: jogador_model, propriedade: propriedade_model) -> None:
        """Comportamento de um jogador cauteloso dentro da simulação de Banco Imobiliário

        Args:
            jogador (jogador_model): o jogador que esta fazendo a ação
            propriedade (propriedade_model): a propriedade onde o jogador se encontra
        """
        if jogador.saldo >= propriedade.valor_compra and jogador.saldo >= 80:
            self.comprar_propriedade(jogador, propriedade)

    def jogador_aleatorio(self, jogador: jogador_model, propriedade: propriedade_model) -> None:
        """Comportamento de um jogador aleatório dentro da simulação de Banco Imobiliário

        Args:
            jogador (jogador_model): o jogador que esta fazendo a ação
            propriedade (propriedade_model): a propriedade onde o jogador se encontra
        """
        if jogador.saldo >= propriedade.valor_compra and random.randrange(0, 1) == 1:
            self.comprar_propriedade(jogador, propriedade)

    def comprar_propriedade(self, jogador: jogador_model, propriedade: propriedade_model) -> None:
        """Método para simularb a compra de uma propriedade dentro do Banco Imobiliário

        Args:
            jogador (jogador_model): o jogador que esta fazendo a compra
            propriedade (propriedade_model): a propriedade que esta sendo comprada
        """
        propriedade.proprietario = jogador
        jogador.saldo -= propriedade.valor_compra

    def simular(self) -> str:
        """Serviço de simulação de partidas de Banco Imobiliário

        Returns:
            str: string a ser exibida no Console com resultado da simulação
        """
        resultado = ""

        try:
            # Guarda o tempo de início da simulação
            simulacao_comeco = time.time()

            # Cria o objeto que guardará as informações dos resultados
            resultado_partidas = resultado_model()

            # Cria a lista de jogadores a partir dos tipos registrados
            resultado_partidas.jogadores = list[jogador_model]()
            for tj in enum_tipo_jogador:
                resultado_partidas.jogadores.append(jogador_model(tj))

            # Cria as propriedades de acordo com o tamanho do tabuleiro
            propriedades = list[propriedade_model]()
            for i in range(21):
                propriedades.append(propriedade_model(i-1))

            # Faz a simulação de 300 partidas
            for i in range(300):
                resultado_partidas = self.simular_partida(resultado_partidas, propriedades)

            # Antes de retornar os resultados, ordena a lista de jogadores pelo número de vitórias
            resultado_partidas.jogadores.sort(key=lambda j:(j.vitorias), reverse=True)
         
            # Guarda o momento em que a simulação foi terminada e calcula o tempo de execução
            simulacao_fim = time.time()
            resultado_partidas.tempo_execucao = simulacao_fim - simulacao_comeco

            # retorna o resultado formatado no Console
            resultado = get_console_string(resultado_partidas)

        except Exception as e:

            # Caso a simulação dê qualquer tipo de erro, registra a exceção no Console
            resultado = "Erro inexperado: " + str(e)

        return resultado

    def simular_partida(self, resultado_partida: resultado_model, propriedades: list[propriedade_model]) -> resultado_model:
        """Método para simular uma partida inteira de Banco Imobiliário

        Args:
            resultado_partida (resultado_model): resultado da partida atual
            propriedades (list[propriedade_model]): lista de propriedades do tabuleiro

        Returns:
            resultado_model: resultado da partida atualizado
        """
        # Cada partida pode durar no máximo 1000 jogadas
        partidaFinalizada = False

        # Define a ordem dos jogadores e reinicia os parametros
        jogadores_partida = resultado_partida.jogadores[:]
        random.shuffle(jogadores_partida)
        for j in jogadores_partida:
            j.saldo = 300
            j.casa_atual = 0
        for p in propriedades:
            p.proprietario = None

        for i in range(1000):
            resultado_partida.turnos_usados += 1
            partidaFinalizada = self.simular_jogada(jogadores_partida, propriedades)

            # Se o resultado da jogada termina com um vencedor, finaliza o loop
            if partidaFinalizada:
                resultado_partida.total_vitorias += 1
                for r in resultado_partida.jogadores:
                    if(r.tipo == jogadores_partida[0].tipo):
                        r.vitorias += 1
                        break
                break

        # Se passadas as 1000 jogadas e a partida ainda não finalizou, acrescenta-se o número de timeouts
        if partidaFinalizada == False:
            resultado_partida.timeouts += 1

        return resultado_partida

    
    def simular_jogada(self, jogadores: list[jogador_model], propriedades: list[propriedade_model]) -> bool:
        """Método para simular um turno dentro do jogo de Banco Imobiliário

        Args:
            jogadores (list[jogador_model]): lista de jogadores da partida
            propriedades (list[propriedade_model]): lista de propriedades do tabuleiro

        Returns:
            bool: status de vitória dentro do jogo
        """
        partidaFinalizada = False

        for j in jogadores:

            # Em cada jogada o jogador lança um dado de 6 faces
            j.casa_atual += random.randint(1, 6)

            # Se o jogador ultrapassar o número de casas do tabuleiro, recebe 100 em saldo
            if j.casa_atual >= len(propriedades):
                j.casa_atual -= len(propriedades)
                j.saldo += 100

            if(propriedades[j.casa_atual].proprietario != None):
                if j.casa_atual != 0:
                    if(j.saldo >= propriedades[j.casa_atual].valor_aluguel):
                        propriedades[j.casa_atual].proprietario.saldo += propriedades[j.casa_atual].valor_aluguel
                        j.saldo -= propriedades[j.casa_atual].valor_aluguel
                    else:
                        propriedades[j.casa_atual].proprietario.saldo += j.saldo
                        jogadores.remove(j)

                        # Se sobrar apenas 1 jogador, este vence a partida
                        if len(jogadores) == 1:
                            partidaFinalizada = True
                            break
            else:
                acao_jogador = {
                    1 : self.jogador_impulsivo(j, propriedades[j.casa_atual]),
                    2 : self.jogador_exigente(j, propriedades[j.casa_atual]),
                    3 : self.jogador_cauteloso(j, propriedades[j.casa_atual]),
                    4 : self.jogador_aleatorio(j, propriedades[j.casa_atual])
                }
                acao_jogador[int(j.tipo)]

        return partidaFinalizada

def get_console_string(resultado: resultado_model) -> str:
    """Método de ajuda para formatar a resposta dada ao console

    Args:
        resultado (resultado_model): o resultado das partidas

    Returns:
        str: string a ser exibida no Console
    """
    string_final = "\nSimulação realizada em {0} segundos".format(str(resultado.tempo_execucao))
    string_final += "\n\n"
    string_final += "#-------------------------------------------------------------------------#\n"
    string_final += "|              Jogador               |              Vitórias              |\n"
    
    posicao = 0
    for j in resultado.jogadores:
        posicao += 1
        posicao_str = "#{0} Jogador {1}".format(str(posicao), j.tipo.name)
        vitoria_str = str(j.vitorias) + " (" +"%.2f" % (j.vitorias/resultado.total_vitorias * 100) + "%)"
        string_final += "---------------------------------------------------------------------------\n"
        string_final += "|" + f"{posicao_str:^36}" + "|" + f"{vitoria_str:^36}" + "|\n"
    
    media_turnos_str = "%.2f" % (resultado.turnos_usados / 300)
    string_final += "---------------------------------------------------------------------------\n"
    string_final += "|           MÉDIA DE TURNOS          |" + f"{str(media_turnos_str):^36}" + "|\n"
    string_final += "---------------------------------------------------------------------------\n"
    string_final += "|              TIMEOUTS              |" + f"{str(resultado.timeouts):^36}" + "|\n"
    string_final += "#-------------------------------------------------------------------------#\n"

    return string_final

