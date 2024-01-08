import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from generate_data import generate_game_state, print_board
# Check if GPU is available and set device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")

# Define the Tic Tac Toe neural network model
class TicTacToeModel(nn.Module):
    def __init__(self, input_size):
        super(TicTacToeModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(64, 64)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        # x = self.relu1(x)
        # x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

        
def convert_to_numeric(board_row):
    mapping = {"x": 1, "o": -1, "b": 0}
    numeric_board = [mapping[element] for element in board_row]
    return numeric_board

def convert_labels(label):
    return 1 if label.lower() == "positive" else 0

if __name__ == "__main__":
    csv_path = 'tic-tac-toe.data'
    df = pd.read_csv(csv_path)
    # Convert the 9 columns representing the board to a numeric array
    X = torch.tensor([convert_to_numeric(row) for _, row in df.iloc[:, :9].iterrows()], dtype=torch.float32).to(device)
    # Convert the labels in the 10th column to 1s and 0s
    y = torch.tensor(df.iloc[:, 9].apply(convert_labels), dtype=torch.float32).unsqueeze(1).to(device)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Instantiate the model and move it to GPU
    input_size = len(X_train[0])
    # output_size = len(set(y_train.cpu().numpy()))

    print(f"Input Size: {input_size}")
    # print(f"Output Size: {output_size}")
    model = TicTacToeModel(input_size).to(device)

    # Define loss function and optimizer
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    # Training loop
    num_epochs = 15000
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
    torch.save(model.state_dict(), 'tic_tac_toe_model_win.pth')


    # def convert(board_state):
    #     mapping = {" ": 0, "X": 1, "O": -1}
    #     numeric_board = [mapping[element] for element in board_state]
    #     return numeric_board
    # # for _ in range(1000):
    # # new_board, current_player = generate_game_state()
    # new_board, current_player = ["X","0","X","O","X"," ","O"," ","O"], "X"
    # new_board_state = convert(new_board)
    # with torch.no_grad():
    #     model.eval()
    #     new_board_state = torch.tensor(new_board_state, dtype=torch.float32).to(device)
    #     prediction = model(new_board_state)
    #     print(prediction)
    #     result = 1 if prediction[0] > 0.5 else 0

    # print_board(new_board, current_player)
    # print(f'The optimal move is: {result}')

