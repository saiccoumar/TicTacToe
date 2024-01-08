# rng_client.py

import socket
import json
import random 
from tictactoe import TicTacToeGame
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

class State():
    def __init__(self, board, parent, current_player) -> None:
        self.board = board
        self.parent = parent
        self.current_player = current_player
        self.terminal = TicTacToeGame.game_is_over(board)
        self.expanded = self.terminal
        self.num_actions = len([i for i in range(0,len(self.board)) if self.board[i] == " "])
        # V = value of the node and it's children node's values
        self.V = 0  
        # n = number of simulations run from the node. Not to be confused with N, the total number of simulations run 
        self.n = 0
        
        self.children = {}
    
    def __str__(self) -> str:
        return f"State(board={self.board}, current_player={self.current_player}, terminal={self.terminal}, V={self.V}, n={self.n})"
    
    def get_UBT(self, C, N):
        if self.n == 0:
            # Handling the case where n_j is zero to avoid division by zero
            return float("inf")
        log_argument = math.log(N) / self.n if N > 0 and self.n > 0 else 0
        return self.V / self.n + C * math.sqrt(log_argument)

class MCTS():
    def cprint(self, str):
        if self.flag:
            print(str)

    def __init__(self, board, agent_sign="O", C = 2, iterations = 1000, flag = False) -> None:
        self.C = C
        self.N = 0
        self.iterations = iterations
        self.agent_sign = agent_sign
        self.board = board
        self.flag = flag


    def search(self):
        # Initialize board as state
        root = State(self.board, None, self.agent_sign)
   
        # while True:
        for _ in range(self.iterations):
            self.cprint("New iteration")
            # Select Node
            selected_state = self.select(root)
            self.cprint(f"selected node: {str(selected_state)}")
            # Expand
            expanded_state = self.expand(selected_state)
            self.cprint("Expanded")
            # Simulate
            simulation_value = self.rollout(expanded_state)
            self.cprint(f"Rolled Out Value: {simulation_value}")
            # Back Prop
            self.backpropagate(expanded_state, simulation_value)
            self.cprint("Backprogated")

        action , _ = max(root.children.items(), key = lambda x: x[1].get_UBT(self.C, self.N))
        ubt_values_dict = {key: child_state.get_UBT(self.C, self.N) for key, child_state in root.children.items()}
        self.cprint(f"UBT Values: {ubt_values_dict}")

        return action

    def select(self, state):
        # If there are children states that CAN be expand, expand them
        if not state.expanded:
            return state
        else:
            non_terminal_children = [child for child in state.children.values() if not child.terminal]
            if not non_terminal_children:
                return state

            best_child = max(non_terminal_children, key=lambda x: x.get_UBT(self.C, self.N))
            return self.select(best_child)

    
    def expand(self, state):
        if not (state.expanded):
            self.cprint("State not expanded. Expanding")
            open_positions = [i + 1 for i in range(0,len(state.board)) if state.board[i] == " " and ((i+1) not in state.children.keys())]
            child_position = random.choice(open_positions)
            current_player = "O" if state.current_player == "X" else "X"
            child_board = state.board.copy()
            child_board[child_position - 1] = state.current_player
            child_state = State(child_board, state, current_player)
            state.children[child_position] = child_state
            if len(state.children.items()) == state.num_actions:
                state.expanded = True
            self.cprint(f"New State:{str(child_state)}")
            return child_state
        else:
            self.cprint("State expanded. Selecting state.")
            return state


    def rollout(self, state):
        current_simulated_player_turn = state.current_player
        simulated_board = state.board.copy()
        while not (TicTacToeGame.game_is_over(simulated_board)):
            open_positions = [i for i in range(0,len(simulated_board)) if simulated_board[i] == " "]
            simulated_board[random.choice(open_positions)] = current_simulated_player_turn
            current_simulated_player_turn = "O" if current_simulated_player_turn == "X" else "X"
        
        if TicTacToeGame.check_winner(simulated_board, self.agent_sign):
            return 10
        elif TicTacToeGame.check_draw(simulated_board):
            return 5
        elif TicTacToeGame.check_loser(simulated_board, self.agent_sign):
            return -10
        else:
            raise ValueError("Something went wrong!")

    def backpropagate(self, state, value):
        self.N += 1
        while state is not None:
            state.V += value
            state.n += 1 
            state = state.parent
        

    

class MCTSAgent:
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
        print("MCTS AGENT")
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
                print("MCTS Agent won!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("DRAW" in game_state):
                print("It's a draw!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("LOSS" in game_state):
                print("MCTS Agent lost.")
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
        return MCTS(board, player_sign, C=0.7, iterations = 100000, flag=False).search()
        

if __name__ == "__main__":
    # Create a AI client that plays the game using RNG logic. When the game is over, close it's connection to the port.
    client = MCTSAgent()
    client.play_game()
    client.close_connection()
