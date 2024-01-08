# rng_client.py

import socket
import json
import random 
from tictactoe import TicTacToeGame

class OneStepAgent:
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
        print("ONE STEP AGENT")
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
                print("One Step won!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("DRAW" in game_state):
                print("It's a draw!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("LOSS" in game_state):
                print("One Step Agent lost.")
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
        # Check for all open positions (valid choices)
        open_positions = [i + 1 for i in range(0,len(board)) if board[i] == " "]
        
        # Look for wins
        for i in open_positions:
            board_step = board.copy()
            board_step[i-1] = player_sign
            # print("Future board\n-------")
            # Corner_Agent.print_board(board_step)
            if TicTacToeGame.check_winner(board_step, player_sign):
                print("Win detected")
                return i
            
        # Prevent losses
        for i in open_positions:
            board_step = board.copy()
            opp_sign = "O" if player_sign == "X" else "X"

            board_step[i-1] = opp_sign
            # print("Future board\n-------")
            # Corner_Agent.print_board(board_step)
            if TicTacToeGame.check_winner(board_step, opp_sign):
                print("Stop opponent win")
                return i 
        
        

        print("Pick random")
        return random.choice(open_positions)

if __name__ == "__main__":
    # Create a AI client that plays the game using RNG logic. When the game is over, close it's connection to the port.
    client = OneStepAgent()
    client.play_game()
    client.close_connection()
