from game import GoldRush
def set_game():
    matrix = []
    print("Welcome to Gold Rush!")
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    game = GoldRush(rows, cols)
    game.load_board()
    game.print()
    return game

def player_move(player, game):
    direction = input(f"{player}, enter your move (up, down, left, right): ").strip().lower()
    game.move_player(player, direction)
    game.print()
    if game._check_win(player):
        print(f"{player} wins!")
        return True
    return False
        

def run_game(game):
    there_is_a_winner = False
    while not there_is_a_winner:
        for player in ["player1", "player2"]:
            there_is_a_winner = player_move(player, game)
            if there_is_a_winner:
                break


def play_game():
    game = set_game()
    run_game(game)

if __name__ == "__main__":
    play_game()