class TogyzKumalak:
    def __init__(self, 
                 pits_player=[[9 for _ in range(9)] for _ in range(2)],
                 kazan_player = [0, 0],
                 current_player = 0,
                 tuzdyq = [-1, -1],
                 history = []
                 ):
        self.pits_player = pits_player
        self.kazan_player = kazan_player
        self.current_player = current_player
        self.tuzdyq = tuzdyq
        self.history = history

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
            # print("Invalid move: The selected pit is empty.")
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

    def get_legal_moves(self):
        return [i for i in range(9) if self.pits_player[self.current_player][i] != 0]


    def display_board(self):
        print("Current Player: Player", self.current_player + 1)
        for player in range(2):
            print(f"Player {player + 1} pits: {self.pits_player[player]}")
            print(f"Player {player + 1} kazan: {self.kazan_player[player]}")


    def calculate_stones_captured(self, previous_state, current_state):
        """
        Calculate the number of stones captured by the current player in the last move.
        Args:
            previous_state (dict): The game state before the last move.
            current_state (dict): The current game state after the last move.

        Returns:
            int: The number of stones captured by the current player in the last move.
        """
        # Retrieve the kazan counts from both states for the current player
        previous_kazan = previous_state['kazan'][self.current_player]
        current_kazan = current_state['kazan'][self.current_player]

        # Calculate and return the difference
        return current_kazan - previous_kazan


    def step(self, pit_index):
        # Save the current state before making the move for comparison
        state_before_move = self.save_state()

        # Make the move
        valid_move = self.make_move(pit_index)
        if not valid_move:
            return self.save_state(), -50, False  # Penalize invalid move more significantly

        # Check if the game has ended and update the reward
        game_ended = self.check_moves()
        reward = 0  # Initialize reward

        # Calculate the reward based on stones captured if the move was valid
        if valid_move:
            state_after_move = self.save_state()
            stones_captured = self.calculate_stones_captured(state_before_move, state_after_move)
            reward += stones_captured * 5  # Reward 5 points per captured stone

        # Update reward based on game outcome
        if game_ended:
            result = self.game_end()
            if result == "Player 1 Wins":
                reward = 100  # Large reward for winning
            elif result == "Player 2 Wins":
                reward = -100  # Large negative reward if the opponent wins
            else:
                reward = 0  # Neutral reward for a draw
        else:
            # Switch the current player if the game has not ended
            self.current_player = (self.current_player + 1) % 2

        # Return the new state, reward, and whether the game has ended
        return state_after_move, reward, game_ended
    
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
    
class TogyzKumalakAI:
    def __init__(self, player_number, max_depth=3):
        self.player_number = player_number
        self.max_depth = max_depth

    def find_best_move(self, current_game):
        best_move = None
        best_value = float('-inf') #

        for move in current_game.get_legal_moves():
            current_game.make_move(move)
            move_value = self.minimax(current_game, 0, False)
            current_game.undo_move()

            if move_value > best_value: #
                best_value = move_value
                best_move = move

        return best_move

    def minimax(self, current_game, depth, is_maximizing_player):
        if depth == self.max_depth or current_game.check_moves():
            return self.evaluate_game_state(current_game)

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in current_game.get_legal_moves():
                current_game.make_move(move)
                eval = self.minimax(current_game, depth + 1, False)
                current_game.undo_move()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in current_game.get_legal_moves():
                current_game.make_move(move)
                eval = self.minimax(current_game, depth + 1, True)
                current_game.undo_move()
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_game_state(self, current_game):
        # Basic evaluation based on Kazan
        if current_game.current_player == 0:
            score = -(current_game.kazan_player[1] - current_game.kazan_player[0])
        else:
            score = current_game.kazan_player[1] - current_game.kazan_player[0]

        # Additional scoring for Tuzdyq control
        tuzdyq_value = 10  # Adjust this value based on the strategic value of Tuzdyq
        for player in [0, 1]:
            if current_game.tuzdyq[player] != -1:
                if current_game.current_player == player:
                    score += tuzdyq_value
                else:
                    score -= tuzdyq_value
        return score