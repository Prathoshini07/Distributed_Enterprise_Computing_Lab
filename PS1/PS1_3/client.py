import socket
import sys


class TicTacToeClient:
   def __init__(self, host='localhost', port=65432):
       self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.client_socket.connect((host, port))
       self.player_token = self.client_socket.recv(1024).decode()
       print(f"You are player {self.player_token}")
  
   def display_board(self, board):
       """Display the current board state."""
       print("\nCurrent Board:")
       for i in range(0, 9, 3):
           print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
           if i < 6:
               print("-----------")
  
   def play(self):
       try:
           while True:
               # Receive board state
               board_state = self.client_socket.recv(1024).decode().split(',')
               self.display_board(board_state)
              
               # Check for game end conditions
               if board_state[0].startswith('Winner:') or board_state[0] == 'Draw':
                   print(board_state[0])
                   break
              
               # Check if it's the player's turn
               if board_state[0] != 'Winner:' and board_state[0] != 'Draw':
                   while True:
                       try:
                           # Prompt for move
                           move = int(input(f"Player {self.player_token}, enter your move (0-8): "))
                          
                           # Validate move input
                           if 0 <= move <= 8:
                               # Send move to server
                               self.client_socket.send(str(move).encode())
                              
                               # Receive server response
                               response = self.client_socket.recv(1024).decode()
                              
                               if response == 'VALID_MOVE':
                                   break
                               elif response == 'INVALID_MOVE':
                                   print("Invalid move. Try again.")
                           else:
                               print("Invalid input. Please enter a number between 0 and 8.")
                      
                       except ValueError:
                           print("Please enter a valid number.")
      
       except Exception as e:
           print(f"Game error: {e}")
       finally:
           self.client_socket.close()


def main():
   try:
       client = TicTacToeClient()
       client.play()
   except Exception as e:
       print(f"Connection error: {e}")


if __name__ == '__main__':
   main()
