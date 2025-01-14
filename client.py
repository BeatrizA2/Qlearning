import connection as cn
import numpy as np  #usada para criar e manipular a Q-table
import random

#Estabelece a conexão TCP
s = cn.connect(2037)

# Define os hiperparâmetros do Q-Learning
alpha = 0.3  #taxa de aprendizado
gamma = 0.9  #fator de desconto => o quanto o agente leva em conta as recompensas futuras ao tomar uma ação
epsilon = 0.09 #taxa de exploração -> controla a probabilidade de o agente escolher uma ação aleatória em vez de seguir melhor ação conforme o q learning

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
    
    #Se o valor aleatório escolhido for menor que o valor definido para epsilon o personagem escolherá uma ação aleatoriamente
    if rand_num < epsilon:
        # Escolhe uma ação aleatória: 0 - left, 1 - rigth e 2 - jump
        action = random.choice([0, 1, 2])
    else:
        # Escolhe a melhor ação de acordo com a Q-Table
        actions = [0, 1, 2]
        best_action = actions[2] #recebe a ação 2 (pular)
        best_value = Q[state][best_action] #recebe o q-value correspondente ao estado fornecido e a ação 2

        #Verifica qual é a ação que fornece a melhor recompensa para o estado especificado
        for action in actions[:-1]:  #itera sobre o array de ações possíveis sem passar pela ação 2
            value = Q[state][action] #recebe o q-value correspondente ao estado fornecido e a ação definida na iteração
            #verifica se o q value obtido a partir de action é melhor (maior) que o valor salvo em best_value
            #Se for value se torna best_value e a ação desencadeadora se torna a best_action
            if value > best_value:
                best_action = action
                best_value = value
        
        action = best_action #a ação que será retornada recebe a melhor ação

    return action #returna a ação escolhida em formato numérico (0 - left, 1 - rigth e 2 - jump)

reward = 0 #inicializa a variável reward
bk = False #indica se houve uma parada forçada -> ex: matar o terminal
c = 0 #conta a quantidade de vezes que o personagem chegou até a plataforma preta

# Inicia o loop principal do jogo
for i in range(500):
    if bk:
        break
    while True:
        try:
            #Estado do persongem antes da ação
            previous_state = state

            #Escolhe a próxima ação
            action = epsilon_greedy(Q_table, state, epsilon)

            # Obtém o estado pós a ação e a recompensa decorrente
            state, reward = cn.get_state_reward(s, actions[action])
            state = int(state, 2) #transforma o estado em inteiro

            #Atualiza a Q_table
            Q_table[previous_state][action] += alpha * (reward + gamma * np.max(Q_table[state]) - Q_table[previous_state][action])
            print("Estado: ", previous_state, "Ação: ", action, "Recompensa: ", reward, "Novo estado: ", bin(state), "Contador: ", c)
            #Personagem alcança a plataforma preta -> essa situação fornece uma recompensa de 300 pontos
            if reward == 300:
                break
        
        except:
            print(Q_table)
            bk = True
            break
    print("COMPLETOU O JOGO")
    c += 1


#Passa os q values da Q table para o arquivo "resultado.txt"
with open("resultado.txt", "w") as f:
        for line in Q_table:
            line_str = " ".join(str(elem) for elem in line)
            f.write(line_str + "\n")
f.close()
