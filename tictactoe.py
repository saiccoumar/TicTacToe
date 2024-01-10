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
    """
    Check for a win.

    Parameters:
    - board: the game state
    - char: the char of the player. If X is passed in, we evaluate if X is winning, if O is winning we evaluate if O is winning. char must be X or O

    Returns:
    - bool: True the player char winning, False if losing
    
    This does not use self as a parameter so this function can be used by agents
    """
    @staticmethod
    def check_winner(board, char):
        if not isinstance(char, str) or char not in ["X", "O"]:
            raise ValueError(f"Invalid symbol: {char}. It must be 'X' or 'O'.")

        for i in range(0, 3):
            if board[i] == board[i + 3] == board[i + 6] == char:
                return True
            if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] == char:
                return True
        if board[0] == board[4] == board[8] == char:
            return True
        if board[2] == board[4] == board[6] == char:
            return True
        return False
    
    # Logic to check if the game has been lost
    """
    Check for a loss.

    Parameters:
    - board: the game state
    - char: the char of the player. If X is passed in, we evaluate if X is winning, if O is winning we evaluate if O is winning. char must be X or O

    Returns:
    - bool: False the player char winning, True if losing
    
    This does not use self as a parameter so this function can be used by agents
    """
    @staticmethod
    def check_loser(board, char):
        opp_char = ""
        if not isinstance(char, str) or char not in ["X", "O"]:
            raise ValueError(f"Invalid symbol: {char}. It must be 'X' or 'O'.")
        else: 
            opp_char = "O" if char == "X" else "X"

        for i in range(0, 3):
            if board[i] == board[i + 3] == board[i + 6] == opp_char:
                return True
            if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] == opp_char:
                return True
        if board[0] == board[4] == board[8] == opp_char:
            return True
        if board[2] == board[4] == board[6] == opp_char:
            return True
        return False
    
    @staticmethod
    def check_draw(board):
        return (" " not in board)
    
    @staticmethod
    def game_is_over(board):
        # It doesn't matter who won or lost. If one player won, lost, or drew, the game is over
        char = "X"
        return (TicTacToeGame.check_winner(board,char) or TicTacToeGame.check_loser(board, char) or TicTacToeGame.check_draw(board))
    
    @staticmethod
    def detect_fork(board, player_sign):
        opp_sign = "O" if player_sign == "X" else "X"
        # Iterate through each position on the board
        for i in range(len(board)):
            if board[i] == opp_sign:
                # Temporarily place the player's sign in the empty position
                past_board = board.copy()
                past_board[i] = " "
                # Check if the player has won from this position
                if TicTacToeGame.detect_win(past_board, player_sign):
                    return True
        # No fork detected
        return False
    
    @staticmethod
    def detect_win(board, player_sign):
        # Check rows
        for row in range(0, 9, 3):
            if board[row:row+3].count(player_sign) == 2 and board[row:row+3].count(' ') == 1:
                return True

        # Check columns
        for col in range(3):
            if board[col] == board[col+3] == player_sign and board[col+6] == ' ':
                return True
            elif board[col] == board[col+6] == player_sign and board[col+3] == ' ':
                return True
            elif board[col+3] == board[col+6] == player_sign and board[col] == ' ':
                return True

        # Check diagonals
        if board[0] == board[4] == player_sign and board[8] == ' ':
            return True
        elif board[0] == board[8] == player_sign and board[4] == ' ':
            return True
        elif board[4] == board[8] == player_sign and board[0] == ' ':
            return True
        elif board[2] == board[4] == player_sign and board[6] == ' ':
            return True
        elif board[2] == board[6] == player_sign and board[4] == ' ':
            return True
        elif board[4] == board[6] == player_sign and board[2] == ' ':
            return True

        return False

   

if __name__ == "__main__":
    board = [' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    print(TicTacToeGame.check_winner(board,"X"))
    print(TicTacToeGame.check_loser(board,"X"))
    print(TicTacToeGame.check_draw(board))
    print(TicTacToeGame.game_is_over(board))

    board = ["O", "O", "O",
        "X"," X", " ",
        "O","X"," "] 
    player_sign = "O"
        # Example Usage:
    # Assuming 'board' is a one-dimensional array and 'player_sign' is the sign of the player who lost
    if TicTacToeGame.detect_fork(board, player_sign):
        print(f"Player {player_sign} won due to a fork.")
    else:
        print(f"No fork detected for Player {player_sign}.")

    
