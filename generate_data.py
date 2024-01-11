import random
from tictactoe import TicTacToeGame
from minimax_agent import MinimaxAgent
from mcts_agent import MCTSAgent
from combined_rules_agent import CombinedRulesAgent
import csv


def generate_game_state():
    board = [" " for _ in range(9)]

    # Generate a random number of moves between 0 and 8
    num_moves = random.randint(0, 8)

    # Players
    players = ["X", "O"]

    current_player = players[0]
    for _ in range(num_moves):
        future_board = board.copy()
        open_positions = [i for i in range(0,len(future_board)) if board[i] == " "]
        
        move_position = random.choice(open_positions)
        future_board[move_position] = current_player
        if TicTacToeGame.game_is_over(future_board):
            return board, current_player
        board = future_board
        current_player = players[1 - (_ % 2)]
    return board, current_player

def print_board(board, current_player):
        print(f"Current Player: {current_player}")
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("---------")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("---------")
        print(f"{board[6]} | {board[7]} | {board[8]}")

def generate_minimax_data():
    for _ in range(10000):
        # Generate a random game state
        board, current_player = generate_game_state()

        # Print the game state
        print_board(board, current_player)

        # Get the decision from MinimaxAgent
        decision = MinimaxAgent.make_decision(board, current_player)

        # Create or open the CSV file
        with open('tic_tac_toe_records_minimax.csv', mode='a', newline='') as csvfile:
            fieldnames = ['board', 'decision']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # If the file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the current game state and decision to the CSV file
            writer.writerow({'board': ''.join(board), 'decision': decision})
def generate_mcts_data():
    for _ in range(10000):
        # Generate a random game state
        board, current_player = generate_game_state()
        print(_)
        # Print the game state
        # print_board(board, current_player)

        # Get the decision from MinimaxAgent
        decision = MCTSAgent.make_decision(board, current_player)

        # Create or open the CSV file
        with open('tic_tac_toe_records_mcts.csv', mode='a', newline='') as csvfile:
            fieldnames = ['board', 'decision']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # If the file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the current game state and decision to the CSV file
            writer.writerow({'board': ''.join(board), 'decision': decision})

def generate_rule_data():
    for _ in range(10000):
         # Generate a random game state
        board, current_player = generate_game_state()

        # Print the game state
        print_board(board, current_player)

        # Get the decision from MinimaxAgent
        decision = CombinedRulesAgent.make_decision(board, current_player)

        # Create or open the CSV file
        with open('tic_tac_toe_records_minimax.csv', mode='a', newline='') as csvfile:
            fieldnames = ['board', 'decision']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # If the file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the current game state and decision to the CSV file
            writer.writerow({'board': ''.join(board), 'decision': decision})

if __name__ == "__main__":
    generate_minimax_data()
