import socket

def main():
    host = '127.0.0.1'
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            # Receive data from server
            message = client_socket.recv(1024).decode()
            print(message)

            # Check for end of game
            if "Winner" in message or "Draw" in message:
                break

            # Prompt for input if it's the player's turn
            if "Your turn" in message:
                move = input("Enter your move (0-8): ")
                client_socket.send(move.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
