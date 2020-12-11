from app.domain.models.jogador_model import jogador_model

class resultado_model:
    """Modelo de resultado das partidas dentro da simulação do Banco Imobiliário
    """

    tempo_execucao: float
    jogadores: list[jogador_model]
    timeouts: int
    turnos_usados: int
    total_vitorias: int

    def __init__(self):
        self.timeouts = 0
        self.tempo_execucao = 0.0
        self.turnos_usados = 0
        self.total_vitorias = 0