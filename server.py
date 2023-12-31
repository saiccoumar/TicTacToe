# server.py

import socket
import threading
from tictactoe import TicTacToeGame
import json

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print("Server is listening for connections...")
        self.players = []
        self.game = TicTacToeGame()
        self.current_player_index = 0
        self.num_players_connected = 0

    def send_game_state(self, player_socket):
        game_state = {
            'board': self.game.board.copy(),
            'current_player': self.game.current_player
        }
        json_data = json.dumps(game_state)
        print(f"Sending game state to Player {self.players.index(player_socket) + 1}: {json_data}")
        player_socket.send(json_data.encode())


    def handle_client(self, client_socket):
        player_number = self.players.index(client_socket) + 1
        client_socket.send(str(player_number).encode())

        self.num_players_connected += 1

        while self.num_players_connected < 2:
            pass

        # for player_socket in self.players:
        client_socket.send("GAME STARTED".encode())

        self.send_game_state(client_socket)

        while True:
            print("Move made.")
            try:
                print("pn:" + str(player_number))
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                if data.isdigit():
                    position = int(data)
                    if 1 <= position <= 9 and self.game.make_move(position):
                        self.game.print_board()
                        if self.game.check_winner():
                            client_socket.send("WIN".encode())
                            loser_socket = self.players[(self.current_player_index + 1) % 2]
                            loser_socket.send("LOSS".encode())
                            break
                        elif " " not in self.game.board:
                            client_socket.send("DRAW".encode())
                            loser_socket = self.players[(self.current_player_index + 1) % 2]
                            loser_socket.send("DRAW".encode())
                            break
                        else:
                            self.game.switch_player()
                            for player in self.players:
                                self.send_game_state(player)
                            self.current_player_index = (self.current_player_index + 1) % 2
                    else:
                        client_socket.send("INVALID_MOVE".encode())
                        self.send_game_state(client_socket)
                        continue
            except ValueError:
                client_socket.send("INVALID_MOVE".encode())
                self.send_game_state(client_socket)
                continue
                            
            except Exception as e:
                print(e)
                break

        print(f"Connection from {client_socket.getpeername()} has been closed.")
        client_socket.close()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} has been established.")
            self.players.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server = Server()
    threading.Thread(target=server.accept_connections).start()
