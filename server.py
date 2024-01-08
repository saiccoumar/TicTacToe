# server.py

import socket
import threading
from tictactoe import TicTacToeGame
import json


# Server Class
class Server:
    def __init__(self):
        # initialize server socket with localhost ip address on port 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print("Server is listening for connections...")
        # Array for player socket
        self.players = []
        # Game imported from tictactoe
        self.game = TicTacToeGame()
        self.current_player_index = 0
        self.num_players_connected = 0

    # Function to send game state from the server to the client. Game state includes the board information as well as whose turn it is. Game state info is in json format
    def send_game_state(self, player_socket):
        game_state = {
            'board': self.game.board.copy(),
            'current_player': self.game.current_player
        }
        json_data = json.dumps(game_state)
        print(f"Sending game state to Player {self.players.index(player_socket) + 1}: {json_data}")
        player_socket.send(json_data.encode())

    # Logic that the server runs to interact with the clients and handle game management
    def handle_client(self, client_socket):
        player_number = self.players.index(client_socket) + 1
        client_socket.send(str(player_number).encode())

        self.num_players_connected += 1

        # Wait for 2 players before interacting with the client further
        while self.num_players_connected != 2:
            pass

        # Send game start code
        client_socket.send("GAME STARTED".encode())

        # Send initial board to clients
        self.send_game_state(client_socket)

        while True:
            print("Move made.")
            try:
                print("pn:" + str(player_number))
                # Wait for players' move 
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                if data.isdigit():
                    # Convert player input to tictactoe move and check for wins, losses, draws
                    position = int(data)
                    if 1 <= position <= 9 and self.game.make_move(position):
                        self.game.print_board()
                        board = self.game.board.copy() 
                        if self.game.check_winner(self.game.board, self.game.current_player):
                            client_socket.send(f"WIN:{json.dumps(board)}".encode())
                            loser_socket = self.players[(self.current_player_index + 1) % 2]
                            loser_socket.send(f"LOSS:{json.dumps(board)}".encode())
                            # End while loop when game is over
                            break
                        elif " " not in self.game.board:
                            client_socket.send(f"DRAW:{json.dumps(board)}".encode())
                            loser_socket = self.players[(self.current_player_index + 1) % 2]
                            loser_socket.send(f"DRAW:{json.dumps(board)}".encode())
                            # End while loop when game is over
                            break
                    # If the game has not ended, and the move is valid, swap players and send the new game state to BOTH players 
                        else:
                            self.game.switch_player()
                            for player in self.players:
                                self.send_game_state(player)
                            self.current_player_index = (self.current_player_index + 1) % 2
                    # If the move is invalid restart the turn 
                    else:
                        client_socket.send("INVALID_MOVE".encode())
                        self.send_game_state(client_socket)
                        continue
            # If the move is invalid restart the turn 
            except ValueError:
                client_socket.send("INVALID_MOVE".encode())
                self.send_game_state(client_socket)
                continue
            # Exception in case there is an error 
            except Exception as e:
                print(e)
                break
        
        # Decrement the connected clients counter when a client disconnects
        self.num_players_connected -= 1

        # Check if all clients have disconnected and exit the server if so
        if self.num_players_connected == 0:
            print("All clients disconnected. Closing the server.")
            exit()

        # Close connection to client when the game is over
        print(f"Connection from {client_socket.getpeername()} has been closed.")
        client_socket.close()

    def accept_connections(self):
        # Repeatedly check for clients that will join
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} has been established.")
            # Add clients to players array for reference later
            self.players.append(client_socket)
            # Start a new thread for each client
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

            

if __name__ == "__main__":
    # Start server and accept connections on a separate thread
    server = Server()
    # Threading optional but included
    threading.Thread(target=server.accept_connections).start()
