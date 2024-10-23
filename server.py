import socket
import threading
import os

# Server settings
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345
BUFFER_SIZE = 4096

# Handle communication between sender and receiver
def handle_client(conn, addr, clients):
    print(f"Connected by {addr}")

    try:
        # Receive the file name length first
        filename_length = int(conn.recv(4).decode())  # Send 4 bytes for the filename length
        filename = conn.recv(filename_length).decode()  # Receive the filename based on its length
        print(f"Receiving file: {filename}")

        # Ensure the received directory exists
        os.makedirs('received', exist_ok=True)

        # Open the file for writing in the received folder
        with open(f'received/{filename}', 'wb') as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)

        print(f"File {filename} received from {addr}")

        # Notify all clients except the sender
        for client in clients:
            if client != conn:
                with open(f'received/{filename}', 'rb') as f:
                    while True:
                        chunk = f.read(BUFFER_SIZE)
                        if not chunk:
                            break
                        client.sendall(chunk)

    except Exception as e:
        print(f"Error handling client {addr}: {e}")

    finally:
        conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    clients = []

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        client_thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        client_thread.start()

if __name__ == "__main__":
    start_server()
