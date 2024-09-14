import socket
import threading
import hashlib

# Server configuration
HOST = '192.168.1.10'
PORT = 5050

# Dictionary to store registered users
users = {}
active_users = {}
# Global dictionary to store conversation partners
conversations = {}

# Function to send message to a conversation partner
def send_message(sender, message):
    recipient = conversations.get(sender)
    if recipient:
        try:
            active_users[recipient].send(f"From {sender}: {message}".encode())
        except Exception as e:
            print(f"Failed to send message to {recipient}: {e}")
    else:
        print("No conversation partner found.")

# Main function to handle client connections
def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    username = None
    # Send a welcome message
    client_socket.send("Welcome to the secure chat system! Please login or register.".encode())

    while True:
        data = client_socket.recv(1024).decode()
        command, *parts = data.split()

        if command == "register":
            # Register new user
            if len(parts) != 2:
                client_socket.send("Invalid syntax. Usage: register <username> <password>".encode())
            else:
                username = parts[0]
                password = hashlib.sha256(parts[1].encode()).hexdigest()  # Hash the password
                if username in users:
                    client_socket.send("Username already exists. Please choose a different one.".encode())
                else:
                    users[username] = password
                    active_users[username] = client_socket
                    client_socket.send("Registration successful!".encode())

        elif command == "login":
            # Login existing user
            if len(parts) != 2:
                client_socket.send("Invalid syntax. Usage: login <username> <password>".encode())
            else:
                username = parts[0]
                # print(username)
                password = hashlib.sha256(parts[1].encode()).hexdigest()  # Hash the password
                # print(password)
                if username in users and users[username] == password and username not in active_users:
                    client_socket.send("Login successful!".encode())
                    active_users[username] = client_socket
                else:
                    client_socket.send("Invalid username or password.".encode())

        elif command == "msg" and username:
            recipient = parts[0]
            message = ' '.join(parts[1:])
            if recipient == conversations.get(username):
                send_message(username, message)
            else:
                client_socket.send("You are not allowed to message this user.".encode())
                
        elif command == "start_chat" and username:
            recipient = parts[0]
            if recipient in active_users and conversations.get(username) is None:
                conversations[username] = recipient
                client_socket.send(f"Chat started with {recipient}.".encode())
                if conversations.get(recipient) is None:
                    conversations[recipient] = username
                active_users[recipient].send(f"{username} initiated chat with you exclusively".encode())
            else:
                client_socket.send("Failed to start chat.".encode())

        elif command == "end_chat" and username:
            if conversations.get(username):
                recipient = conversations.get(username)
                del conversations[recipient]
                del conversations[username]
                client_socket.send("Chat ended.".encode())
                active_users[recipient].send("Chat ended.".encode())
            else:
                client_socket.send("No active chat found.".encode())

        elif command == "exit":
            # Close connection
            print(f"[DISCONNECTED] {address} disconnected.")
            break
        
        elif command == ".":
            continue
        
        else:
            client_socket.send(f"Invalid command. {username}".encode())

    if username:
        del active_users[username]
    client_socket.close()

# Main function to start the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    main()
