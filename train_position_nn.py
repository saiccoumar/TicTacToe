import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from generate_data import generate_game_state, print_board
from sklearn.model_selection import train_test_split
# Check if GPU is available and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")

# Define the Tic Tac Toe neural network model
class TicTacToeModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(TicTacToeModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 256)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(256, output_size)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.tanh(x)
        return x

# Function to convert board states to numerical format
def convert_to_numeric(board_state):
    mapping = {" ": 0, "X": 1, "O": -1}
    numeric_board = [mapping[element] for element in board_state]
    return numeric_board

if __name__ == "__main__":
    csv_path1 = 'tic_tac_toe_records_minimax.csv'
    df1 = pd.read_csv(csv_path1)
    csv_path2 = 'tic_tac_toe_records_mcts.csv'
    df2 = pd.read_csv(csv_path1)
    csv_path3 = 'tic_tac_toe_records_combined_rules.csv'
    df3 = pd.read_csv(csv_path1)
    df =  pd.concat([df1, df2, df3], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
    # Dummy data (replace this with your actual dataset)
    X = torch.tensor([convert_to_numeric(board_state) for board_state in df["board"]], dtype=torch.float32).to(device)
    y = torch.tensor(df["decision"]-1, dtype=torch.long).to(device)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Instantiate the model and move it to GPU
    input_size = len(X_train[0])
    output_size = len(set(y_train.cpu().numpy()))
    print(f"Input Size: {input_size}")
    print(f"Output Size: {output_size}")
    model = TicTacToeModel(input_size, output_size).to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # Training loop
    num_epochs = 5000
    for epoch in range(num_epochs):
        # Forward pass
        outputs = model(X_train)
        loss = criterion(outputs, y_train)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Print progress
        if (epoch+1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
        with torch.no_grad():
            model.eval()
            test_outputs = model(X_test)
            test_loss = criterion(test_outputs, y_test)
            print(f'Test Loss: {test_loss.item():.4f}')

    # Save the trained model if needed
    torch.save(model.state_dict(), 'tic_tac_toe_model_position.pth')

    # # Use the trained model for predictions
    # # Move new_board_state to GPU if available
    # # new_board, current_player = generate_game_state()
    # new_board, current_player = ["X","X","X","O","X"," ","O"," ","O"], "X"
    # new_board_state = convert_to_numeric(new_board)
    # with torch.no_grad():
    #     model.eval()
    #     new_board_state = torch.tensor(new_board_state, dtype=torch.float32).to(device)
    #     prediction = model(new_board_state)
    #     optimal_move = torch.argmax(prediction).item()

    # print_board(new_board, current_player)
    # print(f'The optimal move is: {optimal_move}')
