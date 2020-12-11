from app.domain.models.jogador_model import jogador_model

class propriedade_model:
    """Modelo de propriedade dentro da simulação do Banco Imobiliário
    """
    
    valor_compra = 0
    valor_aluguel = 0
    proprietario: jogador_model = None

    def __init__(self, index: int):
        self.valor_compra = index * 10
        self.valor_aluguel = index * 5