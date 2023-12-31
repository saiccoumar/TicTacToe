# rng_client.py

import socket
import json
import random 

class RNGClient:
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
        print(f"You are Player {self.player_number}")

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
                    position = self.make_decision(game_state['board'])
                    print(f"Position: {position}")
                    self.send_message(str(position))
                else:
                    print("Waiting for the other player's move...")
            # If the move is invalid, the player is prompted again
            elif isinstance(game_state, str) and game_state == "INVALID_MOVE":
                print("Invalid move. Please try again.")
                continue
            # Break when the game is won, drawn, or lost
            elif isinstance(game_state, str) and game_state == "WIN":
                print("Congratulations! You won!")
                break
            elif isinstance(game_state, str) and game_state == "DRAW":
                print("It's a draw!")
                break
            elif isinstance(game_state, str) and game_state == "LOSS":
                print("Sorry, you lost.")
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
    def make_decision(board):
        # Check for all open positions (valid choices)
        open_positions = []
        for i in range(0,len(board)):
            if board[i] == " ":
                # Board is indexed 1-9, who thought that would be a good idea...
                open_positions.append(i+1)
        # Pick a random spot
        return random.choice(open_positions)

if __name__ == "__main__":
    # Create a AI client that plays the game using RNG logic. When the game is over, close it's connection to the port.
    client = RNGClient()
    client.play_game()
    client.close_connection()
