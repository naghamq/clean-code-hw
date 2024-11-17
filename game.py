from Matrix import Matrix
import random

MIN_COINS = 10
POINT = 10
WINNING_SCORE = 100

class GoldRush(Matrix):
    WALL = "wall"
    COIN = "coin"
    EMPTY = "."

    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.player1_score = 0
        self.player2_score = 0
        self.winner = ""
        self.total_coins = 0

    def load_board(self):
        """Initializes the board with a random distribution of walls, coins, and empty spaces."""
        if self.rows == 0 or self.cols == 0:
            self.matrix = []
            return

        self.matrix = []
        elements = [self.COIN, self.EMPTY, self.WALL]
        coin_count = 0

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                element = self._generate_element(elements)
                row.append(element)
                if element == self.COIN:
                    coin_count += 1
            self.matrix.append(row)

        self._place_players()
        self._adjust_for_coins(coin_count)
        self.total_coins = coin_count

        if coin_count < MIN_COINS:
            return self.load_board()

        return self.matrix

    def _generate_element(self, elements):
        """Randomly chooses an element to place on the board."""
        return random.choice(elements)

    def _place_players(self):
        """Places the players on the board."""
        self.matrix[0][0] = "player1"
        self.matrix[self.rows - 1][self.cols - 1] = "player2"

    def _adjust_for_coins(self, coin_count):
        if coin_count < MIN_COINS:
            self.load_board()

    def move_player_in_direction(self, player, direction):
        current_position = self._find_player_position(player)
        if current_position:
            row, col = current_position
            move_methods = {
                "up": self._move_up,
                "down": self._move_down,
                "left": self._move_left,
                "right": self._move_right
            }
            move_function = move_methods.get(direction)
            if move_function:
                move_function(row, col, player)

    def _find_player_position(self, player):
        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                if value == player:
                    return i, j
        return None

    def _move(self, row, col, player, delta_row, delta_col):
        other_player = self._get_other_player(player)
        new_row, new_col = row + delta_row, col + delta_col

        if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
            return

        if self.matrix[new_row][new_col] not in [self.WALL, other_player]:
            if self.matrix[new_row][new_col] == self.COIN:
                self._increase_score(player)
            self.matrix[row][col] = self.EMPTY
            self.matrix[new_row][new_col] = player

        return self._check_win(player)

    def _get_other_player(self, player):
        return "player2" if player == "player1" else "player1"

    def _move_up(self, row, col, player):
        return self._move(row, col, player, -1, 0)

    def _move_down(self, row, col, player):
        return self._move(row, col, player, 1, 0)

    def _move_left(self, row, col, player):
        return self._move(row, col, player, 0, -1)

    def _move_right(self, row, col, player):
        return self._move(row, col, player, 0, 1)

    def _increase_score(self, player):
        if player == "player1":
            self.player1_score += POINT
        else:
            self.player2_score += POINT

        print(f"{player} score: {getattr(self, f'player{player[-1]}_score')}")

    def _check_win(self, player):
        if getattr(self, f'player{player[-1]}_score') >= WINNING_SCORE:
            self.winner = player
            return self.winner
