import connection as cn
import numpy as np
import random

#Estabelece a conexão TCP
s = cn.connect(2037)

# Define os hiperparâmetros do Q-Learning
alpha = 0.5
gamma = 0.9
epsilon = 0.25

#Define o número de colunas (número de possíveis ações) e o número de linhas (possíveis estados) da Q table
num_actions = 3
num_possible_states = 96

#Estado inicial do Amongois
state = 0

#Array das possíveis ações do personagem
actions = ["left", "right", "jump"]

#Iniacializa a Q-table com todos os elementos iguais a zero
Q_table = np.zeros((num_possible_states, num_actions))


#Função que escolhe a próxima ação a ser tomada
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
        # Escolhe uma ação aleatória: 0 - left, 1 - rigth e 2 - jump
        action = random.choice([0, 1, 2])
    else:
        # Escolhe a melhor ação de acordo com a Q-Table
        actions = [0, 1, 2]
        best_action = actions[0]
        best_value = Q[state][best_action]

        #Verifica qual é a ação que fornece a melhor recompensa para o estado especificado
        for action in actions[1:]:
            value = Q[state][action]
            if value > best_value:
                best_action = action
                best_value = value

        action = best_action

    return action

# Inicia o loop principal do jogo
while True:
    #Estado do persongem antes da ação
    previous_state = state

    #Escolhe a próxima ação
    action = epsilon_greedy(Q_table, state, epsilon)

    # Obtém o estado pós a ação e a recompensa decorrente
    state, reward = cn.get_state_reward(s, actions[action])
    state = int(state, 2) #transforma o estado em inteiro

    #Atualiza a Q_table
    Q_table[previous_state][action] += alpha * (reward + gamma * np.max(Q_table[state]) - Q_table[previous_state][action])

    #Condição de parada: personagem alcança a plataforma preta - recompensa de 300 pontos
    if(reward == 300):
        break

#Passa os q values da Q table para o arquivo "resultado.txt"
with open("resultado.txt", "w") as f:
        for line in Q_table:
            line_str = " ".join(str(elem) for elem in line)
            f.write(line_str + "\n")
f.close()