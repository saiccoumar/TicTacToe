# Tic Tac Toe

<p align="center">
 <img size="100%" src="https://github.com/saiccoumar/TicTacToe/assets/55699636/d465be6f-2fab-4ed4-9bd3-73c60a43ba31">
 by Sai Coumar
</p>

## Introduction
Welcome to my Tic Tac Toe implementation! 
This project was actually a proof of concept for future projects with the simplest game I could possibly use. Using a simple game serves as a reference for more complicated algorithms that use the same algorithms (like poker!) and hopefully will make working on those projects easier. The idea here is to make an OOP Client/Server python version of the game so that AI Clients can be easily implemented and participate in the game like player clients without needing to change the game logic every time we test a new algorithm. In this project, I implemented TicTacToe, and then experimented with different AIs that would play the game - either against each other or against the player. In this README I'll cover how to use this project as well as some of the implementation details along with pseudocode for the algorithms. In my medium article, I'll compare performances and explain more about the theory behind the AI and how each algorithm stacked up against AI. 

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

Let's add some degree of intelligence. The most basic AIs, rule-based agents, use pre-determined policies defined by domain experts to make generalized selections. Since tic tac toe is a "solved game", and any human with a brain can figure out a good strategy, making a viable rule-based AI is pretty easy. 

#### Center Agent
The first rule I tried was always playing the center square every single time. 
```
def make_decision(board, player_sign):
        # Check for all open positions (valid choices)
        open_positions = [i + 1 for i in range(0,len(board)) if board[i] == " "]   
        # If center is empty pick     
        if board[4] == " ":
            print("Pick Center")
            return 5

        print("Pick random")
        return random.choice(open_positions)
```
If the rule cannot be met, we default to random choices. Center choice wins pretty often against RNG client, but can still lose. It essentially aims to subset the game state space to all boards where the bot has played the center, which generally has a higher win rate than the entire set of all game states. This rule is pretty weak and a smart agent could still outmaneuver this pretty easily.

#### Corner Agent
```
def make_decision(board, player_sign):
        opp_sign = "O" if player_sign == "X" else "X"
        # Check for all open positions (valid choices)
        open_positions = [i + 1 for i in range(0,len(board)) if board[i] == " "]

        for i in range(0,9,2):
            if board[i] == " " and board[8-i] == opp_sign:
                return i+1
        # If corners are empty pick a corner
        corners = [i+1 for i in range(0,9,2)] 
        if board[0] == " " or board[2] == " " or board[6] == " " or board[8] == " ":
            print("Pick Corner")
            return random.choice(corners) 

        print("Pick random")
        return random.choice(open_positions)
```
This agent aims to take corners opposite to the opponent's corners, and take any other corners that are available. This aims to create forks, where a player has 2 winning options and the opponent can only block one leading to a win. The corner agent can win often, but is vulnerable to the possibility that an agent picks the middle three positions horizontally or vertically because the corner agent will pick corners for the first 2-4 rounds. When corner agent wins, it wins by a blowout but when it loses it loses hard. 

#### One Step Agent
```
def make_decision(board, player_sign):
        # Check for all open positions (valid choices)
        open_positions = [i + 1 for i in range(0,len(board)) if board[i] == " "]
        
        # Look for wins
        for i in open_positions:
            board_step = board.copy()
            board_step[i-1] = player_sign
            if TicTacToeGame.check_winner(board_step, player_sign):
                print("Win detected")
                return i
            
        # Prevent losses
        for i in open_positions:
            board_step = board.copy()
            opp_sign = "O" if player_sign == "X" else "X"

            board_step[i-1] = opp_sign\
            if TicTacToeGame.check_winner(board_step, opp_sign):
                print("Stop opponent win")
                return i 

        print("Pick random")
        return random.choice(open_positions)
```
One Step Agent is the first agent that actually tries to look for opportunities to win and prevent a loss. It goes through all the possible turns that the player can make on the current board and returns a position if it can result in an immediate win. Similarly it goes through all possible turns that the opponent can make and returns a position if the opponent can result in an immediate win, thereby preventing that win. Since it goes "one step" into the future to evaluate moves, I named it the One Step Agent.

One step works REALLY well. RNG struggles against it and even later algorithms that we'll cover struggle. One-step unequivocally has the best foresight of what will happen in exactly one move - even better than later algorithms we'll discuss. Unfortunately if an opponent sets up a fork more than one step into the future, One-step cannot detect it and can still lose. We'll address this with the MCTS and minimax algorithms.   

#### Combined Rules Agent
```
def make_decision(board, player_sign):
        # Check for all open positions (valid choices)
        open_positions = [i + 1 for i in range(0,len(board)) if board[i] == " "]
        opp_sign = "O" if player_sign == "X" else "X"
        # Look for forks
        # If center is empty pick     
        if board.count(" ") == 8:
            print("Pick Center")
            return 5
        
        for i in open_positions:
            board_step = board.copy()
            board_step[i-1] = player_sign
            # Check if the current move creates a fork
            fork_created = False
            for j in open_positions:
                if j != i:
                    board_step_fork = board_step.copy()
                    board_step_fork[j-1] = opp_sign
                    if TicTacToeGame.check_winner(board_step_fork, player_sign):
                        fork_created = True
                        break
            if fork_created:
                return i

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
            board_step[i-1] = opp_sign
            # print("Future board\n-------")
            # Corner_Agent.print_board(board_step)
            if TicTacToeGame.check_winner(board_step, opp_sign):
                print("Stop opponent win")
                return i 
      
        # If corners are empty pick a corner
        corners = [i+1 for i in range(0,9,2)] 
        if board[0] == " " or board[2] == " " or board[6] == " " or board[8] == " ":
            print("Pick Corner")
            return random.choice(corners) 

        print("Pick random")
        return random.choice(open_positions)
```

Combined Rules Agent combines the rules of the previous agent as well as a new rule that looks for forks. This agent is VERY strong. Many of the rules compliment each other; corner agent had an issue where it would never pick the center and lose, but with fork and one-step before the corners and center rules after, that vulnerability is covered. The one-step struggled with getting outplayed by forks but the forking logic before covers the vulnerability of that move. Combined Rules performed well against every other bot, but struggled against humans. Humans can pick up on the rules that the agent was using and exploit them very quickly. Tic Tac Toe is a "solved" game so it's possible to make rules to ALWAYS win, but if those rules aren't used then a rules based agent will always be vulnerable to an exploit. This is something we can try to tackle with algorithms aren't rule based.

#### Monte Carlo Tree Search
The first algorithm we'll look at is the Monte Carlo Tree Search algorithm. You've likely heard of this one before - it's famously used for chess engines and board games across the world and I made this my starting point because of it's reputation.
```
class MCTS():
def search(self):
        # Initialize board as state
        root = State(self.board, None, self.agent_sign)
   
        # while True:
        for _ in range(self.iterations):
            self.cprint("New iteration")
            # Select Node
            selected_state = self.select(root)

            # Expand
            expanded_state = self.expand(selected_state)

            # Simulate
            simulation_value = self.rollout(expanded_state)
            
            # Back Prop
            self.backpropagate(expanded_state, simulation_value)
           

        action = best_action(state.actions)
        return action

    ...

class State():
    def __init__(self, board, parent, current_player) -> None:
        self.board = board
        # V = value of the node and it's children node's values
        self.V = 0  
        # n = number of simulations run from the node. Not to be confused with N, the total number of simulations run 
        self.n = 0
        ...
    
    def get_UBT(self, C, N):
        if self.n == 0:
            # Handling the case where n_j is zero to avoid division by zero
            return float("inf")
        log_argument = math.log(N) / self.n if N > 0 and self.n > 0 else 0
        return self.V / self.n + C * math.sqrt(log_argument)


def make_decision(board, player_sign):
        return MCTS(board, C=0.7, iterations = 100000).search()
```
MCTS is a bit complicated and took the most debugging. The general intuition is pretty simple: the monte carlo search tree will add another level of depth, simulate results, and backpropagate results back to previous states. If it reaches the all terminal cases, it will continue sampling to make results more accurate. The benefit of this is that you can run it for however long you want and ALWAYS get a result WITHOUT a complete exhaustive tree search. If you only have resources for 5 iterations, you can only expand 5 states and still get a result. If you have resources for 1,000,000 iterations it will give you a result. This is better than exhaustive search algorithms like minimax which cannot get results unless it finishes searching the entire tree which can be impossible in games like Go which has possible state spaces that are too large to compute. 
The steps:
1. Select a state to expand
2. Expand the state
3. "Rollout" the state and get the result of the simulation
4. Backpropagate the results throughout the tree
5. Repeat for N iterations
The exact specifics of the selection and expansion criteria are very intricate and if you're really interested, I'd recommend examining mcts_agent.py itself. Also, be very careful with other implementations of MCTS. Many implementations will have mistakes (such as expanding the entire tree immediately or using an incorrect UBT equation) and the algorithm will still function but very poorly.

Unfortunately, the MCTS algorithm is still pretty mediocre. After implementing the algorithm, I found that MCTS required more computational resources and wasn't very effective because Tic Tac Toe has such a small game state space. While it wasn't inherently bad, other agents happened to be comparable with much less resources. It consistently beat the weaker agents but was matched evenly with agents like the combined rules agent and minimax.

Let's consider why this is the case with the combined rules agent. In the endgame, where there are only 1 or 2 moves left in the game, MCTS is doing thousands of simulations and making approximate heuristics whereas the Combined rules agent is exhaustively checking the states and deterministically pick the objectively best option with the fork and one-step rules. This is unique to Tic Tac Toe, because the game is so simple and is considered "solved" but in a game like Chess or Go, rule agents and exhaustive searches cannot generalize such a large game state space as well as MCTS. 

#### Minimax
With the benefit of hindsight, let's use an exhaustive search with better decision making than combined rules.
```
class Minimax():

    def evaluation_function_1(self, state):
        if win:
            return 10
        elif loss:
            return -10 
        elif draw:
            return 0
        
    def evaluation_function_2(self, state):
        if win:
            if win by fork:
                return 20
            return 10
        elif loss:
            if loss by fork:
                return -20
            return -10 
        elif draw:
            return 0
        
    def max_value(self, state, alpha, beta):
        v = float("-inf")
        if state.terminal:
            # v = self.evaluation_function_1(state)
            v = self.evaluation_function_1(state)       
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
            v = self.evaluation_function_1(state)    
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

        return max(max_actions, key=lambda action: min_max_values[action])

    def make_decision(board, player_sign):        
        return Minimax(board, player_sign).search() + 1
```

Minimax is a very straightforward algorithm. Minimax aims to find the sequence of moves that minimize opponents benefit and maximize the agents benefit. To do this we recursively call minimize and maximize functions on each other until reaching terminal states. The terminal state values are evaluated by an evaluation function. Originally I used an evaluation function that would reward winning, penalize losing, and do nothing for a draw. Unfortunately this reward system led to a lot of states being equal in value, so I added a bigger reward for wins by fork and a bigger penalty for loss by fork. I also included alpha/beta pruning in my minimax implementation to improve efficiency.

Minimax also had an issue where it would keep picking the exact same state at the beginning and leading to certain outcomes every time against rule based agents. This is because when there are tied values the max() function always picks the first instance. By using random choices to break ties, this makes it possible to win and lose in different ways rather than lose the same time over and over. This would be solved if my evaluation function was more nuanced, but minimax is already the most exhaustive algorithm I'll use in this entire project and I didn't want it to get any worse with a complex evaluation function but minimax had a bad habit of blundering some very simple moves. 
