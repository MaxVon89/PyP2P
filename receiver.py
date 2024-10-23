import socket
import os

# Receiver settings
SERVER_HOST = '127.0.0.1'  # IP of the server
SERVER_PORT = 12345
BUFFER_SIZE = 4096

# Function to receive files from the server
def receive_file():
    # Create a socket and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))

        # Receive the filename length (first 4 bytes)
        filename_length = int(s.recv(4).decode())  # Read the 4-byte filename length
        filename = s.recv(filename_length).decode()  # Read the filename based on its length
        print(f"Receiving file: {filename}")

        # Create the received directory if it doesn't exist
        os.makedirs('received', exist_ok=True)

        # Open the file for writing in the received folder
        with open(f'received/{filename}', 'wb') as f:
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)

        print(f"File '{filename}' received and saved in the 'received' directory.")

if __name__ == "__main__":
    receive_file()
