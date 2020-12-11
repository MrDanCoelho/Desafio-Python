debug=True

from app.services.simulation_service import simulation_service

print("Bem vindo à simulação de Banco Imobiliário")

mensagem_ajuda = "Para rodar uma simulação, escreva \"run\". Para sair, digite \"exit\""
print(mensagem_ajuda)

comando = ""

while comando != "exit":
    comando = input()

    if comando == "run":
        service = simulation_service()
        print(service.simular())
    else:
        print(mensagem_ajuda)