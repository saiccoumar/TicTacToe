import torch
from train_win_nn import TicTacToeModel
from train_position_nn import convert_to_numeric
import pandas as pd
import socket
import json
import random 
from combined_rules_agent import CombinedRulesAgent
from one_step_agent import OneStepAgent
from minimax_agent import MinimaxAgent

class NeuralNetworkPredictor():
    # Input size and output size were checked via print statements during train
    def __init__(self, input_size = 9) -> None:
        self.model = TicTacToeModel(input_size)
        self.model.load_state_dict(torch.load('tic_tac_toe_model_win.pth'))
        self.model.eval()
    
    def predict(self, new_board_state):
        with torch.no_grad():
            # Convert new board to numeric format
            numeric_board = convert_to_numeric(new_board_state)
            new_board_tensor = torch.tensor(numeric_board, dtype=torch.float32)
            
            # Make prediction
            prediction = self.model(new_board_tensor)
            return prediction
            

class NNWinPredictorAgent:
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
        print("PREDICT WIN AGENT")
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
                    nn_predictor = NeuralNetworkPredictor() 
                    position = self.make_decision(game_state['board'], self.player_sign, nn_predictor)
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
                print("Predict Win Agent won!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("DRAW" in game_state):
                print("It's a draw!")
                final_board = json.loads(game_state.split(":")[1])
                self.print_board(final_board)
                break
            elif isinstance(game_state, str) and ("LOSS" in game_state):
                print("Predict Win Agent lost.")
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
    def make_decision(board, player_sign, nn_predictor):
        # Check for all open positions (valid choices)
        open_positions = [i + 1 for i in range(0,len(board)) if board[i] == " "]
        if len(open_positions) > 4:
            # return OneStepAgent.make_decision(board, player_sign)
            # return CombinedRulesAgent.make_decision(board, player_sign)
            return MinimaxAgent.make_decision(board, player_sign)

        predicted_scores = {}
        for i in open_positions:
            future_board = board.copy()
            future_board[i-1] = player_sign
            predicted_scores[i] = nn_predictor.predict(future_board) 
        choices = [key for key, value in predicted_scores.items() if value == 1]
        print("Endgame Detected.")

        if len(predicted_scores.items())>0:
            print(predicted_scores)
            return max(predicted_scores, key=predicted_scores.get)

        print("NN failed to yield a valid choice")
        return random.choice(open_positions)

if __name__ == "__main__":
    # Create a AI client that plays the game using RNG logic. When the game is over, close it's connection to the port.
    client = NNWinPredictorAgent()
    client.play_game()
    client.close_connection()