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
