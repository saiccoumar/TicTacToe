class TicTacToeGame:
    def __init__(self):
        # One dimensional array representing the board
        # [ 1 2 3 
        #   4 5 6
        #   7 8 9 ]
        self.board = [" " for _ in range(9)]
        # Player using X starts first
        self.current_player = "X"

    # Prints the board
    def print_board(self):
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("---------")
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("---------")
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")

    # If the position is valid, the position on the board is marked with the current players symbol
    def make_move(self, position):
        if 1 <= position <= 9 and self.board[position - 1] == " ":
            self.board[position - 1] = self.current_player
            return True
        return False

    # Switch the symbol to mark on the board when players turns swap
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    # Logic to check if the game has been won
    def check_winner(self):
        for i in range(0, 3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != " ":
                return True
            if self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2] != " ":
                return True
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return True
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return True
        return False
