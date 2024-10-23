import socket
import os

# Sender settings
SERVER_HOST = '127.0.0.1'  # IP of the server
SERVER_PORT = 12345
BUFFER_SIZE = 4096

# Function to send a file to the server
def send_file(filename):
    # Check if file exists in the uploads directory
    filepath = os.path.join('uploads', filename)
    if not os.path.exists(filepath):
        print(f"File '{filename}' not found in uploads directory.")
        return

    # Create socket and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))

        # Send the filename length (4 bytes) and the filename itself
        filename_length = len(filename)
        s.send(str(filename_length).zfill(4).encode())  # Send filename length as 4-byte string
        s.send(filename.encode())  # Send the actual filename

        # Open the file and send its content
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                s.sendall(data)

        print(f"File '{filename}' sent to the server.")

if __name__ == "__main__":
    filename = input("Enter the file name to send (from uploads directory): ")
    send_file(filename)
