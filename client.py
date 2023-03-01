import connection as cn
import numpy as np
import random

s = cn.connect(2037)

# Define os hiperparâmetros do Q-Learning
alpha = 0.5
gamma = 0.9
epsilon = 0.25

num_actions = 3
num_possible_states = 96

state = 0


Q_table = np.zeros((num_possible_states, num_actions))

# Cria um array com as possíveis ações do personagem 
actions = ["left", "rigth", "jump"]


# Define a função para escolher a próxima ação a ser tomada
def epsilon_greedy(Q, state, epsilon):
    """
    Implementação da política epsilon-greedy.

    Args:
        Q (dict): Dicionário contendo a Q-Table com as estimativas de recompensa.
        state (str): Estado atual do jogo.
        epsilon (float): Valor da taxa de exploração.

    Returns:
        action (str): Ação a ser tomada pelo personagem Amongois.
    """

    # Gera um número aleatório entre 0 e 1
    rand_num = random.uniform(0, 1)

    if rand_num < epsilon:
        # Escolhe uma ação aleatória
        action = random.choice(["left", "right", "jump"])
    else:
        # Escolhe a melhor ação de acordo com a Q-Table
        actions = ["left", "right", "jump"]
        best_action = actions[0]
        best_value = Q[state][best_action]

        for action in actions[1:]:
            value = Q[state][action]
            if value > best_value:
                best_action = action
                best_value = value

        action = best_action

    return action

# Inicia o loop principal do jogo
while True:
    previous_state = state
    # Obtém o estado atual e a recompensa
    state, reward = cn.get_state_reward(s, action)

    #Escolhe a próxima ação
    next_action = epsilon_greedy(Q_table, state, epsilon)
    action = actions.index(next_action)


    Q_table[previous_state, action] += alpha * (reward + gamma * np.max(Q_table[state, :]) - Q_table[previous_state, action])
    print(Q_table)
