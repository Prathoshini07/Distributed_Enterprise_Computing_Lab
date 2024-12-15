import socket
import threading
import time


class TicTacToeGame:
   def __init__(self):
       self.board = [' '] * 9
       self.current_player = 'X'
  
   def make_move(self, position, player):
       """Validate and make a move on the board."""
       if self.board[position] == ' ':
           self.board[position] = player
           return True
       return False
  
   def check_winner(self):
       """Check if there's a winner or a draw."""
       # Winning combinations
       win_combinations = [
           # Rows
           (0, 1, 2), (3, 4, 5), (6, 7, 8),
           # Columns
           (0, 3, 6), (1, 4, 7), (2, 5, 8),
           # Diagonals
           (0, 4, 8), (2, 4, 6)
       ]
      
       for combo in win_combinations:
           if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]) and self.board[combo[0]] != ' ':
               return self.board[combo[0]]
      
       # Check for draw
       if ' ' not in self.board:
           return 'Draw'
      
       return None


class GameSession(threading.Thread):
   def __init__(self, player1_socket, player2_socket):
       threading.Thread.__init__(self)
       self.player1_socket = player1_socket
       self.player2_socket = player2_socket
       self.game = TicTacToeGame()
  
   def run(self):
       try:
           # Assign tokens and notify players
           self.player1_socket.send('X'.encode())
           self.player2_socket.send('O'.encode())
          
           while True:
               # Player X's turn
               self.handle_player_turn(self.player1_socket, 'X', self.player2_socket)
              
               # Check for game end after X's move
               winner = self.game.check_winner()
               if winner:
                   self.end_game(winner)
                   break
              
               # Player O's turn
               self.handle_player_turn(self.player2_socket, 'O', self.player1_socket)
              
               # Check for game end after O's move
               winner = self.game.check_winner()
               if winner:
                   self.end_game(winner)
                   break
      
       except Exception as e:
           print(f"Game session error: {e}")
       finally:
           self.player1_socket.close()
           self.player2_socket.close()
  
   def handle_player_turn(self, current_player_socket, player_token, other_player_socket):
       """Handle a single player's turn."""
       # Send current board state
       board_state = ','.join(self.game.board)
       current_player_socket.send(board_state.encode())
      
       # Receive move from current player
       move = int(current_player_socket.recv(1024).decode())
      
       # Validate move
       if self.game.make_move(move, player_token):
           # Send confirmation to current player
           current_player_socket.send('VALID_MOVE'.encode())
          
           # Send updated board to other player
           board_state = ','.join(self.game.board)
           other_player_socket.send(board_state.encode())
       else:
           # Send invalid move notification
           current_player_socket.send('INVALID_MOVE'.encode())
           # Recursive call to retry the turn
           self.handle_player_turn(current_player_socket, player_token, other_player_socket)
  
   def end_game(self, winner):
       """End the game and notify players of the result."""
       result_msg = f'Winner:{winner}' if winner != 'Draw' else 'Draw'
       self.player1_socket.send(result_msg.encode())
       self.player2_socket.send(result_msg.encode())


class TicTacToeServer:
   def __init__(self, host='localhost', port=65432):
       self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.server_socket.bind((host, port))
       self.server_socket.listen(10)  # Allow multiple game sessions
       print(f"Server started on {host}:{port}")
  
   def start(self):
       try:
           while True:
               # Wait for first player
               print("Waiting for first player...")
               player1_socket, player1_address = self.server_socket.accept()
               print(f"First player connected from {player1_address}")
              
               # Wait for second player
               print("Waiting for second player...")
               player2_socket, player2_address = self.server_socket.accept()
               print(f"Second player connected from {player2_address}")
              
               # Create and start a new game session
               game_session = GameSession(player1_socket, player2_socket)
               game_session.start()
      
       except Exception as e:
           print(f"Server error: {e}")
       finally:
           self.server_socket.close()


def main():
   server = TicTacToeServer()
   server.start()


if __name__ == '__main__':
   main()
