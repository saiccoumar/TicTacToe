# rng_client.py

import socket
import json
import random 
from tictactoe import TicTacToeGame


class State():
    def __init__(self, board, current_player) -> None:
        self.board = board
        opp_sign = "O" if current_player == "X" else "X"
        self.current_player = current_player
        self.terminal = TicTacToeGame.game_is_over(board)
        self.expanded = self.terminal
        self.successors = {}
        for i in range(0,len(self.board)):
            if self.board[i] == " ":
                future_board = self.board.copy()
                future_board[i] = current_player   
                self.successors[i] = State(future_board, opp_sign)
        # V = value of the node based on it's children node's valuesi
        self.V = None
        
class Minimax():
    def __init__(self, board, ai_player_sign) -> None:
        self.board = board
        self.ai_player_sign = ai_player_sign

    def evaluation_function_1(self, state):
        if TicTacToeGame.check_winner(state.board, self.ai_player_sign):
            return 10
        elif TicTacToeGame.check_loser(state.board, self.ai_player_sign):
            return -10 
        elif TicTacToeGame.check_draw(state.board):
            return 0
        
    def evaluation_function_2(self, state):
        if TicTacToeGame.check_winner(state.board, self.ai_player_sign):
            if TicTacToeGame.detect_fork(state.board, self.ai_player_sign):
                return 20
            return 10
        elif TicTacToeGame.check_loser(state.board, self.ai_player_sign):
            if TicTacToeGame.detect_fork(state.board, "O" if self.ai_player_sign == "X" else "X"):
                return -20
            return -10 
        elif TicTacToeGame.check_draw(state.board):
            return 0
        
    def max_value(self, state, alpha, beta):
        v = float("-inf")
        if state.terminal:
            # v = self.evaluation_function_1(state)
            v = self.evaluation_function_2(state)
            return v
        
        for _ , successor in state.successors.items():
            v = max(v, self.min_value(successor, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        
        return v
    
    def min_value(self, state, alpha, beta):
        v = float("inf")
        if state.terminal:
            # v = self.evaluation_function_1(state)
            v = self.evaluation_function_2(state)
            return v
        
        for _ , successor in state.successors.items():
            v = min(v, self.max_value(successor, alpha, beta))
            if v <=  alpha:
                return v
            beta = min(beta, v)
        
        return v
    
    def search(self):
        alpha, beta = float("-inf"), float("inf")
        root = State(self.board, self.ai_player_sign)

        for _, successor in root.successors.items():
            score = self.min_value(successor, alpha, beta)
            successor.V = score

        # Collect actions with their corresponding minimax values
        min_max_values = {key: child_state.V for key, child_state in root.successors.items()}

        # Shuffle actions with the same minimax value to introduce randomness
        max_actions = [action for action in min_max_values.keys() if min_max_values[action] == max(min_max_values.values())]
        random.shuffle(max_actions)

        print(f"Minimax Values: {min_max_values}")
        return max(max_actions, key=lambda action: min_max_values[action])



class MinimaxAgent:
    def __init__(self):
        # initialize cliennt socket with localhost ip address on port 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.client_socket.connect((self.host, self.port))
        self.player_number = int(self.client_socket.recv(1024).decode())
        # Player 1 uses X and Player 2 uses O
        self.player_sign = "X"
        if self.player_number != 1:
            self.player_sign = "O"
        print("MINIMAX AGENT")
        print(f"You are Player {self.player_number}")
        print(f"Your sign is {self.player_sign}")

    # Client messages Server
    def send_message(self, message):
        self.client_socket.send(message.encode())

    # Server messages Client
    def receive_data(self):
        data = self.client_socket.recv(1024).decode()
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
        
    


    # Logic to play the game 
    def play_game(self):
        while True:
            game_state = self.receive_data()
            # Wait for start code
            if isinstance(game_state, str) and game_state == "GAME STARTED":
                print("Game has started!")
            # If the data is the board, make a move
            elif isinstance(game_state, dict):
                print("Current Board:")
                self.print_board(game_state['board'])
                print(f"Current Player: {game_state['current_player']}")

                if game_state['current_player'] == f"{self.player_sign}":
                    # instead of getting the position from the player, let the program decide what position to pick
                    position = self.make_decision(game_state['board'], self.player_sign)
                    print(f"Position: {position}")
                    self.send_message(str(position))
                else:
                    print("Waiting for the other player's move...")
            # If the move is invalid, the player is prompted again
            elif isinstance(game_state, str) and game_state == "INVALID_MOVE":
                print("Invalid move. Please try again.")
                continue
            # Break when the game is won, drawn, or lost
            elif isinstance(game_state, str) and ("WIN" in game_state):
                print("Minimax won!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("DRAW" in game_state):
                print("It's a draw!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("LOSS" in game_state):
                print("Minimax Agent lost.")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
                
    # Close client socket
    def close_connection(self):
        self.client_socket.close()

    # Helper method similar to tictactoe class
    @staticmethod
    def print_board(board):
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("---------")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("---------")
        print(f"{board[6]} | {board[7]} | {board[8]}")

    # Logic to choose which position to pick
    @staticmethod
    def make_decision(board, player_sign):
        
        return Minimax(board, player_sign).search() + 1

if __name__ == "__main__":
    # Create a AI client that plays the game using RNG logic. When the game is over, close it's connection to the port.
    client = MinimaxAgent()
    client.play_game()
    client.close_connection()
