from app.domain.enums.enum_tipo_jogador import enum_tipo_jogador


class jogador_model:
    """Modelo de jogador dentro da simulação de Banco Imobiliário
    """

    tipo: enum_tipo_jogador = None
    vitorias = 0
    saldo = 300
    casa_atual = 0

    def __init__(self, tipo: enum_tipo_jogador):
        self.tipo = tipo