# Tic Tac Toe

<p align="center">
 <img size="100%" src="https://github.com/saiccoumar/TicTacToe/assets/55699636/d465be6f-2fab-4ed4-9bd3-73c60a43ba31">
 by Sai Coumar
</p>

## Introduction
Welcome to my Tic Tac Toe implementation! 
This project was actually a proof of concept for future projects with the simplest game I could possibly use. The idea is to make an OOP Client/Server python version of the game and that AI Clients can be easily implemented and participate in the game like player clients. In this project, I implemented TicTacToe, and then experimented with different AIs that would play the game - either against each other or against the player. In this README I'll cover how to use this project as well as some of the implementation details. In my medium article, I'll compare performances and explain more about the theory behind the AI and how each algorithm stacked up against AI. 

To play Tic Tac Toe, start the server by running 
```
python server.py
```
in one terminal. Then run
```
python client.py
```
in two other terminals. Each player uses a terminal to play the game. 

Alternatively,
```
python *ai*.py
```
can be substituted for the clients to have the automated AI play for that terminal. You can have AIs in both terminals and they'll play against each other. The AI files available are: rng_agent.py, center_agent.py, corner_agent.py, one_step_agent.py, combined_rules_agent.py, mcts_agent.py, minimax_agent.py, predict_win_nn.py, and predict_position_nn.py.

The start scripts automate executing these three functions. Modify them to run the commands with your desired client/agents if you'd like to save yourself a little typing while testing!

## Implementation
### Running the Game
<p align="center">
 <img width="75%" height=auto src="https://github.com/saiccoumar/TicTacToe/assets/55699636/16ed5b25-8ed2-4822-9569-3b01a115e812">
</p>

#### Server

```
class Server:
    def __init__(self):
        ...

    # Function to send game state from the server to the client. Game state includes the board information as well as whose turn it is. Game state info is in json format
    def send_game_state(self, player_socket):
        ...

    # Logic that the server runs to interact with the clients and handle game management
    def handle_client(self, client_socket):
        if players have joined
        start
        while True:
            move = get_move()
            if game_over:
                 # inform client
                 break
            else:
                 # send game state to client
        ...

    def accept_connections(self):
        ...

            

if __name__ == "__main__":
    server = Server()
    threading.Thread(target=server.accept_connections).start()
```
The server essentially manages the game. The server class waits for clients to join, accepts their connection, and begins the game when 2 players have joined. Once the game starts (the "GAME START" code & initial game state has been sent to the clients) it loops and waits for the clients response. If a client responds, it checks if their move is valid, then checks if someone has won. If someone has won, the game ends and the clients are informed that the game is over and who won. If the game isn't over, it sends the updated game state to the client and waits for the next move. Check out the implementation if you're interested in making a Client/Server game!

#### Clients/Agents
```
class Agent:
    def __init__(self):
        ...

    # Client messages Server
    def send_message(self, message):
        ...

    # Server messages Client
    def receive_data(self):
        return data_recieved

    # Logic to play the game 
    def play_game(self):
        while True:
            game_state = receive_data()
            # Wait for start code
            if game_state == "GAME STARTED":
                print("Game has started!")

            # If the data is the board, make a move
            elif isinstance(game_state, dict):
                print("Current Board: board")

                if player_turn:
                    position = make_decision()
                    send_message(position)

            # If the move is invalid, the player is prompted again
            elif game_state == "INVALID_MOVE":
                print("Invalid move. Please try again.")
                continue

            # Break when the game is won, drawn, or lost
            elif game_state == "WIN":
                print("RNG Agent won!")
                break
            elif game_state == "DRAW":
                print("It's a draw!")
                break
            elif game_state == LOSS":
                print("RNG Agent lost.")
                break
                
    # Close client socket
    def close_connection(self):
        ...

    # Logic to choose which position to pick
    def make_decision(board):
        ...
        return decision

if __name__ == "__main__":
    # Create a AI client that plays the game using RNG logic. When the game is over, close it's connection to the port.
    client = Agent()
    client.play_game()
    client.close_connection()
```
The client and every agent has this setup. The client waits for the game state or status codes from the server and acts when it's their turn. Each AI agent uses a different method for make_decision while client simply takes input from a user prompt in the terminal. This design is why the agents are modular and we can play the game with different agents without reconfiguring the game logic. 

### AI Agent Decision making
![image](https://github.com/saiccoumar/TicTacToe/assets/55699636/913446e6-aede-4b68-ad81-504e06c58ff4)
Every agent uses this setup with a different "black box". Let's go over how each of make their decisions inside their "black boxes"

#### RNG Agent
Starting with the simplest option, we have the most naive approach to tic tac toe: picking a random open square.
```
def make_decision(board):
        # Check for all open positions (valid choices)
        open_positions = []
        for i in range(0,len(board)):
            if board[i] == " ":
                open_positions.append(i+1)
        
        return random.choice(open_positions)
```
This approach has a very low "intelligence" but serves as a good control. It is possible to win by making random choices but with any more intelligence, an AI will be able to consistently beat the random choice agent. If the random choice agent is winning against another AI, then that AI is likely bugged and needs to be reworked. 
