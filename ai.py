class TogyzKumalakAI:
    def __init__(self, player_number, max_depth=3):
        self.player_number = player_number
        self.max_depth = max_depth

    def find_best_move(self, current_game):
        best_move = None
        best_value = float('-inf')

        for move in current_game.get_legal_moves():
            current_game.make_move(move)
            move_value = self.minimax(current_game, 0, False)
            current_game.undo_move()

            if move_value > best_value:
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

