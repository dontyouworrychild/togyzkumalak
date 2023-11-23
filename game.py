class TogyzKumalak:
    def __init__(self):
        self.pits_player = [[9 for _ in range(9)] for _ in range(2)]
        self.kazan_player = [0, 0]
        self.current_player = 0
        self.tuzdyq = [-1, -1]
        self.history = []

    def reset_game(self):
        self.pits_player = [[9 for _ in range(9)] for _ in range(2)]
        self.kazan_player = [0, 0]
        self.current_player = 0
        self.tuzdyq = [-1, -1]
        self.history = []

    def game_end(self):
        if self.kazan_player[0] > self.kazan_player[1]:
            return "Player 1 Wins"
        elif self.kazan_player[0] < self.kazan_player[1]:
            return "Player 2 Wins"
        else:
            return "Draw"

    def check_moves(self):
        end = all(pit == 0 for pit in self.pits_player[self.current_player])
        if end:
            opponent = (self.current_player + 1) % 2
            self.kazan_player[opponent] += 162 - sum(self.kazan_player)
            return True
        return False

    def save_state(self):
        return {
            'pits': [[pit for pit in player_pits] for player_pits in self.pits_player],
            'kazan': self.kazan_player.copy(),
            'tuzdyq': self.tuzdyq.copy(),
            'current_player': self.current_player
        }

    def make_move(self, pit_index):
        if self.pits_player[self.current_player][pit_index] == 0:
            print("Invalid move: The selected pit is empty.")
            return False

        state_before_move = self.save_state()
        self.history.append(state_before_move)

        stones = self.pits_player[self.current_player][pit_index]
        self.pits_player[self.current_player][pit_index] = 0
        temp_player = self.current_player

        # Special case handling for single stone
        if stones == 1:
            if pit_index == 8:
                if self.tuzdyq[(self.current_player + 1) % 2] == 0:
                    self.kazan_player[self.current_player] += 1
                else:
                    self.pits_player[(self.current_player + 1) % 2][0] += 1
                    temp_player = (self.current_player + 1) % 2
                    pit_index = 0
            else:
                if self.tuzdyq[self.current_player] == pit_index + 1:
                    self.kazan_player[(self.current_player + 1) % 2] += 1
                else:
                    self.pits_player[self.current_player][pit_index + 1] += 1
                    pit_index += 1
            stones -= 1
            # self.pits_player[self.current_player][pit_index] = 0
            
        while stones > 0:
            
            if temp_player == self.current_player and pit_index == self.tuzdyq[(self.current_player + 1) % 2]:
                self.kazan_player[(self.current_player + 1) % 2] += 1
                stones -= 1
                continue    

            self.pits_player[temp_player][pit_index] += 1
            stones -= 1

            # Handling the last stone and tuzdyk capture rules
            if stones == 0:
                captured = self.pits_player[temp_player][pit_index]
                if temp_player != self.current_player and (captured == 2 or captured == 3) and self.tuzdyq[temp_player] == -1:
                    self.kazan_player[self.current_player] += captured
                    self.pits_player[temp_player][pit_index] = 0
                    if captured == 3:
                        self.tuzdyq[temp_player] = pit_index
                elif temp_player != self.current_player and self.pits_player[temp_player][pit_index] % 2 == 0:
                    self.kazan_player[self.current_player] += self.pits_player[temp_player][pit_index]
                    self.pits_player[temp_player][pit_index] = 0



            if pit_index == 8:
                temp_player = (temp_player + 1) % 2
                pit_index = -1

            pit_index = (pit_index + 1) % 9
        
        return True

    def undo_move(self):
        if not self.history:
            print("No moves to undo.")
            return False

        last_state = self.history.pop()
        # print(last_state)

        self.pits_player = last_state['pits']
        self.kazan_player = last_state['kazan']
        self.tuzdyq = last_state['tuzdyq']
        self.current_player = last_state['current_player']
        return True

    def get_legal_moves(self):
        """
        Get a list of legal moves for the current player.
        A move is legal if the pit index is between 0 and 8 (inclusive),
        and the pit is not empty.
        """
        return [i for i in range(9) if self.pits_player[self.current_player][i] != 0]


    def display_board(self):
        print("Current Player: Player", self.current_player + 1)
        for player in range(2):
            print(f"Player {player + 1} pits: {self.pits_player[player]}")
            print(f"Player {player + 1} kazan: {self.kazan_player[player]}")

    def play(self):
        while True:
            self.display_board()
            pit_index = int(input(f"Player {self.current_player + 1}, choose a pit (1-9): ")) - 1
            if not self.make_move(pit_index):
                continue

            if self.check_moves():
                print(self.game_end())
                break
            self.current_player = (self.current_player + 1) % 2

from ai import TogyzKumalakAI

game = TogyzKumalak()
# ai1 = TogyzKumalakAI(0, 0)
ai2 = TogyzKumalakAI(1, 3)

while True:
    game.display_board()

    if game.current_player == 0:
        # move = ai1.find_best_move(game)
        move = int(input(f"Choose a pit (1-9): ")) - 1
        if not game.make_move(move):
            continue
    elif game.current_player == 1:
        move = ai2.find_best_move(game)
        if not game.make_move(move):
            continue

    if game.check_moves():
        print(game.game_end())
        break

    game.current_player = (game.current_player + 1) % 2
