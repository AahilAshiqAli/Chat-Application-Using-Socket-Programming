import tkinter as tk
from tkinter import messagebox
import socket
from PIL import ImageTk, Image
import threading

# Server configuration
SERVER_HOST = '192.168.1.10'
SERVER_PORT = 5050

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        # Set window size to fill the entire screen
        self.root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

        # Load background image
        self.bg_image = Image.open("bg.jpeg")
        self.bg_image = self.bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Canvas widget and place the background image on it
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Load logo image and resize it
        logo_image = Image.open("LOGO.png")
        logo_image = logo_image.resize((200, 200), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        # Set window icon
        self.root.iconphoto(True, self.logo_photo)

        # Load another image for the logo
        logo2_image = Image.open("logo1.png")
        logo2_image = logo2_image.resize((200, 200), Image.LANCZOS)
        self.logo2_photo = ImageTk.PhotoImage(logo2_image)

        # Create a label for the logo image with transparent background
        self.logo2_label = tk.Label(root, image=self.logo2_photo, bg=self.root.cget("bg"))
        self.logo2_label.place(relx=0.5, rely=0.2, anchor="center")

        # Create labels, entry fields, and buttons
        self.label_username = tk.Label(root, text="Username:", font=("Arial", 18, "bold"), bg="white")
        self.label_username.place(relx=0.5, rely=0.4, anchor="center")
        self.entry_username = tk.Entry(root, font=("Arial", 16, "bold"))
        self.entry_username.place(relx=0.5, rely=0.45, anchor="center")
        self.entry_username.configure(background="#FFFFFF")

        self.label_password = tk.Label(root, text="Password:", font=("Arial", 18, "bold"), bg="white")
        self.label_password.place(relx=0.5, rely=0.5, anchor="center")
        self.entry_password = tk.Entry(root, show="*", font=("Arial", 16, "bold"))
        self.entry_password.place(relx=0.5, rely=0.55, anchor="center")
        self.entry_password.configure(background="#FFFFFF")

        self.btn_login = tk.Button(root, text="Login", command=self.login, font=("Arial", 14, "bold"), relief="flat")
        self.btn_login.place(relx=0.5, rely=0.6, anchor="center", width=180, height=30)

        self.btn_register = tk.Button(root, text="Register", command=self.register, font=("Arial", 14, "bold"), relief="flat")
        self.btn_register.place(relx=0.5, rely=0.65, anchor="center", width=180, height=30)

        # Create a socket for the client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER_HOST, SERVER_PORT))

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.send_message(f"login {username} {password}")

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.send_message(f"register {username} {password}")
        response = self.receive_message()
        if response == "Registration successful!":
            messagebox.showinfo("Success", response)
            # Open chat window after successful registration
            self.start_chat_client()
        else:
            messagebox.showerror("Error", response)


    def send_message(self, message):
        try:
            self.client.send(message.encode())
            response = self.receive_message()
            if response == "Login successful!" or response == "Registration successful!":
                messagebox.showinfo("Success", response)
                # Open chat window if login or registration successful
                self.start_chat_client()
            else:
                messagebox.showerror("Error", response)
        except Exception as e:
            print(f"Error occurred while sending message: {e}")

    def receive_message(self):
        return self.client.recv(1024).decode()

    def start_chat_client(self):
        # Close the login window
        self.root.destroy()

        # Create the chat window
        chat_window = tk.Tk()
        chat_window.title("Chat Application Window")

        # Set the chat window to fullscreen
        chat_window.geometry("{0}x{1}+0+0".format(chat_window.winfo_screenwidth(), chat_window.winfo_screenheight()))
        
        # Load the background image
        bg_image = tk.PhotoImage(file="bg1.jpeg")

        # Create a label with the background image
        bg_label = tk.Label(chat_window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Create the message list
        self.message_list = tk.Text(chat_window, width=50, height=20)
        self.message_list.pack()

        # Create the message entry field
        self.entry_message = tk.Entry(chat_window, width=50)
        self.entry_message.pack()

        # Create the send button
        btn_send = tk.Button(chat_window, text="Send", command=self.send_chat_message)
        btn_send.pack()

        # Create a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive_chat_message)
        receive_thread.start()

        # Run the chat window
        chat_window.mainloop()

    def start_chat_client(self):
        # Close the login window
        self.root.destroy()

        # Create the chat window
        chat_window = tk.Tk()
        chat_window.title("Chat Application Window")

        # Set window size to fill the entire screen
        chat_window.geometry("{0}x{1}+0+0".format(chat_window.winfo_screenwidth(), chat_window.winfo_screenheight()))


        # Create the message list with larger font size
        self.message_list = tk.Text(chat_window, width=130, height=34, font=("Arial", 12))
        self.message_list.pack()

        # Create the message entry field
        self.entry_message = tk.Entry(chat_window, width=130, font=("Arial", 12,"bold"))
        self.entry_message.pack()

        # Create the send button with larger font size
        btn_send = tk.Button(chat_window, text="Send", command=self.send_chat_message, font=("Arial", 14, "bold"))
        btn_send.pack()

        # Create a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive_chat_message)
        receive_thread.start()

        # Run the chat window
        chat_window.mainloop()

    def send_chat_message(self):
        message = self.entry_message.get()
        self.client.send(message.encode())
        self.entry_message.delete(0, tk.END)

    def receive_chat_message(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == "exit":
                    messagebox.showinfo("Info", "The other user has left the chat.")
                    self.client.close()  # Close the client's connection
                    break  # Exit the loop
                self.update_chat_window(message)
            except:
                break

    def update_chat_window(self, message):
        self.message_list.insert(tk.END, message + "\n")
        self.message_list.see(tk.END)  # Scroll to the bottom of the message list

def main():
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()


