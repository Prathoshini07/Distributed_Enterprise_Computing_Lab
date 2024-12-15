import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_turn = 'X'

    def display_board(self):
        """Return the board as a string for display."""
        board = f"\n {self.board[0]} | {self.board[1]} | {self.board[2]} \n"
        board += "---|---|---\n"
        board += f" {self.board[3]} | {self.board[4]} | {self.board[5]} \n"
        board += "---|---|---\n"
        board += f" {self.board[6]} | {self.board[7]} | {self.board[8]} \n"
        return board

    def make_move(self, position, player):
        """Make a move if the position is valid and return success status."""
        if 0 <= position < 9 and self.board[position] == ' ':
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        """Check for a winner or draw."""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return f"Winner: Player {self.board[combo[0]]}"

        if ' ' not in self.board:
            return "Draw"

        return None  # Game continues


def handle_session(player1, player2):
    """Handle a game session between two players."""
    game = TicTacToe()
    players = {player1: 'X', player2: 'O'}
    current_socket = player1

    # Notify players of their tokens
    player1.send("You are Player 1 (X)".encode())
    player2.send("You are Player 2 (O)".encode())

    while True:
        # Send the board to both players
        board = game.display_board()
        for player in [player1, player2]:
            player.send(board.encode())

        # Notify current player
        current_player_token = players[current_socket]
        current_socket.send(f"Your turn, Player {current_player_token}. Enter your move (0-8):".encode())

        try:
            # Receive move and validate
            move = int(current_socket.recv(1024).decode())
            if not game.make_move(move, current_player_token):
                current_socket.send("Invalid move. Try again.".encode())
                continue
        except ValueError:
            current_socket.send("Invalid input. Try again.".encode())
            continue

        # Check for winner or draw
        result = game.check_winner()
        if result:
            board = game.display_board()
            for player in [player1, player2]:
                player.send(board.encode())
                player.send(result.encode())
            break

        # Switch turns
        current_socket = player1 if current_socket == player2 else player2

    player1.close()
    player2.close()


def main():
    host = '127.0.0.1'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Tic-Tac-Toe Server is running...")
    print("Waiting for players...")

    while True:
        player1, addr1 = server_socket.accept()
        print(f"Player 1 connected from {addr1}")

        player2, addr2 = server_socket.accept()
        print(f"Player 2 connected from {addr2}")

        # Start a new session for the two players
        session_thread = threading.Thread(target=handle_session, args=(player1, player2))
        session_thread.start()


if __name__ == "__main__":
    main()
