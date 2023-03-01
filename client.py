import connection as cn
import numpy as np

s = cn.connect()


# Cria um array com as possíveis ações do personagem 
actions = ["left", "rigth", "jump"]

action = ""


# Define os hiperparâmetros do Q-Learning
alpha = ...
gamma = ...
epsilon = ...

# Cria um array com as possíveis ações do personagem 
actions = ["left", "rigth", "jump"]



# Define a função para escolher a próxima ação a ser tomada
def choose_action(state):
    # Implemente aqui a política de escolha de ações (p. ex., epsilon-greedy)

    return action

# Inicia o loop principal do jogo
while True:
    # Obtém o estado atual e a recompensa
    estado, recompensa = cn.get_state_reward(s, action)

    # Atualiza a tabela Q
    next_state = ...
    next_action = choose_action(next_state)

    # Define a próxima ação
    action = next_action