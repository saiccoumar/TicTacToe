# client.py

import socket
import json

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.client_socket.connect((self.host, self.port))
        self.player_number = int(self.client_socket.recv(1024).decode())
        self.player_sign = "X"
        if self.player_number != 1:
            self.player_sign = "O"
        print(f"You are Player {self.player_number}")

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def receive_data(self):
        data = self.client_socket.recv(1024).decode()
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    def play_game(self):
        while True:
            game_state = self.receive_data()
            if isinstance(game_state, str) and game_state == "GAME STARTED":
                print("Game has started!")
            elif isinstance(game_state, dict):
                print("Current Board:")
                self.print_board(game_state['board'])
                print(f"Current Player: {game_state['current_player']}")

                if game_state['current_player'] == f"{self.player_sign}":
                    position = input("Enter your move (1-9): ")
                    self.send_message(position)
                else:
                    print("Waiting for the other player's move...")
            elif isinstance(game_state, str) and game_state == "INVALID_MOVE":
                print("Invalid move. Please try again.")
                continue
            elif isinstance(game_state, str) and game_state == "WIN":
                print("Congratulations! You won!")
                break
            elif isinstance(game_state, str) and game_state == "DRAW":
                print("It's a draw!")
                break
            elif isinstance(game_state, str) and game_state == "LOSS":
                print("Sorry, you lost.")
                break
                

    def close_connection(self):
        self.client_socket.close()

    @staticmethod
    def print_board(board):
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("---------")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("---------")
        print(f"{board[6]} | {board[7]} | {board[8]}")

if __name__ == "__main__":
    client = Client()
    client.play_game()
    client.close_connection()
