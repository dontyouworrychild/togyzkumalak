# import pickle
# import random

# def state_to_tuple(state):
#     # Convert the complex state dictionary into a hashable tuple
#     pits_tuple = tuple(tuple(pits) for pits in state['pits'])
#     kazan_tuple = tuple(state['kazan'])
#     tuzdyq_tuple = tuple(state['tuzdyq'])
#     return (pits_tuple, kazan_tuple, tuzdyq_tuple, state['current_player'])

# class QLearningAgent:
#     def __init__(self, alpha=0.1, gamma=0.99, epsilon=0.2):
#         self.q_table = {}
#         self.alpha = alpha
#         self.gamma = gamma
#         self.epsilon = epsilon

#     def get_q_value(self, state_tuple, action):
#         return self.q_table.get((state_tuple, action), 0)

#     def choose_action(self, state, legal_actions):
#         if not legal_actions:  # Check if the list of legal actions is empty
#             return None  # or handle as needed, perhaps signaling an end-game or invalid state

#         state_tuple = state_to_tuple(state)
#         if random.random() < self.epsilon:
#             return random.choice(legal_actions)  # Explore
#         else:
#             q_values = [self.get_q_value(state_tuple, action) for action in legal_actions]
#             if not q_values:  # Additional check if q_values turns out empty unexpectedly
#                 return None
#             max_q_value = max(q_values)
#             # Exploit: choose the action with the highest Q-value
#             return legal_actions[q_values.index(max_q_value)]


#     def update_q_table(self, state, action, reward, next_state, done, legal_actions):
#         state_tuple = state_to_tuple(state)
#         next_state_tuple = state_to_tuple(next_state)
#         if not done:
#             next_q_values = [self.get_q_value(next_state_tuple, next_action) for next_action in legal_actions]
#             max_next_q = max(next_q_values) if next_q_values else 0
#         else:
#             max_next_q = 0
#         current_q = self.get_q_value(state_tuple, action)
#         new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
#         self.q_table[(state_tuple, action)] = new_q

# def load_agent(filename):
#     with open(filename, 'rb') as f:
#         q_table = pickle.load(f)
#     agent = QLearningAgent()
#     agent.q_table = q_table
#     return agent

# # Example usage:
# agent = load_agent('/senior/togyzkumalak/q_learning_agent.pkl')


# example_of_state = {
#             'pits': [[9 for _ in range(9)] for _ in range(2)],
#             'kazan': [0, 0],
#             'tuzdyq': [-1, -1],
#             'current_player': 0
#         }


# def get_legal_moves(pits_player, current_player):
#     return [i for i in range(9) if pits_player[current_player][i] != 0]
# from game_agent import TogyzKumalak, TogyzKumalakAI    
from .game_agent import TogyzKumalak, TogyzKumalakAI
def ai(state):
    # pits = state['pits']
    # current_player = state['current_player']
    # move = agent.choose_action(state, get_legal_moves(pits, current_player))
    # return move


# print(ai(example_of_state))
    game = TogyzKumalak(pits_player=state['pits'],
                        kazan_player = state['kazan'],
                        current_player = 1,
                        tuzdyq = state['tuzdyq'],
                        history = [])


    # game = TogyzKumalak(pits_player=[[9 for _ in range(9)] for _ in range(2)],
    #                 kazan_player = [0, 0],
    #                 current_player = 0,
    #                 tuzdyq = [-1, -1],
    #                 history = [])
    ai = TogyzKumalakAI(0, state['level'])
    move = ai.find_best_move(game)
    return move