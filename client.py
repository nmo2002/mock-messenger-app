import socket
import threading
import random
import tkinter as tk
import ttkbootstrap as tkb
from tkinter import scrolledtext
import ssl

# client
# SOURCES USED TO:
# THE SOURCES GIVEN IN THE PROJECT INSTRUCTION DOCUMENT...such as the BOGOTOGO.COM and TLS wrapping
# https://www.youtube.com/watch?v=A_Z1lgZLSNc TO UNDERSTAND THREADING...
# https://www.youtube.com/watch?v=bguFKIgEpoM to install openssl
# https://www.youtube.com/watch?v=ibf5cx221hk tkinter introduction video
# https://docs.python.org/3/library/tkinter.html tkinter documentation
# https://snyk.io/blog/implementing-tls-ssl-python/  implement tls steps to understanding...


# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context.load_cert_chain(certfile="clientcert.pem", keyfile="client.pem")
# context.load_verify_locations(cafile="clientcert.pem")
# tried to get TLS to work but, it had a deprecation issue...there was also an issue getting any feedback on client.


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 3351

# client_socket = context.wrap_socket(client_socket, do_handshake_on_connect=True)



def exit_app():
    GUI.chatroom.config(state=tk.NORMAL)
    GUI.chatroom.insert(tk.END, 'You have left the chat...' + '\n')
    GUI.chatroom.config(state=tk.DISABLED)
    print("You have left the chat.")
    client_socket.close()


def listen_to_server(client):
    while True:
        try:
            response = client.recv(2048).decode('utf-8')
        except(OSError, ConnectionAbortedError):
            print('Bye!')
            break
        if response != "":
            name = response.split('->')[0]
            msg = response.split('->')[1]
            GUI.chatroom.config(state=tk.NORMAL)
            GUI.chatroom.insert(tk.END, f'{name}-> {msg}' + '\n')
            GUI.chatroom.config(state=tk.DISABLED)
            print(f'{name}-> {msg}')
        else:
            print(f'Empty message')


def send_to_server():
    while True:
        message = GUI.msg_text.get()
        if message != '':
            if message == '.exit':
                GUI.chatroom.config(state=tk.NORMAL)
                GUI.chatroom.insert(tk.END, 'You have left the chat...' + '\n')
                GUI.chatroom.config(state=tk.DISABLED)
                print("You have left the chat.")
                try:
                    client_socket.sendall(message.encode())
                    client_socket.close()
                    break
                except(OSError, ConnectionAbortedError):
                    GUI.chatroom.config(state=tk.NORMAL)
                    GUI.chatroom.insert(tk.END, 'Client forcefully closed...' + '\n')
                    GUI.chatroom.config(state=tk.DISABLED)
                    print("Client forcefully closed...")
            client_socket.sendall(message.encode())
            GUI.msg_text.delete(0, len(message))
        else:
            break


def client_to_server(client_socket):
    identifier = random.randint(1, 10000)
    print(f'We will give you a random identifier: {identifier}')

    client_name = f'{GUI.user_text.get()}{identifier}'
    if client_name != "":
        client_socket.sendall(client_name.encode())
    else:
        GUI.chatroom.config(state=tk.NORMAL)
        GUI.chatroom.insert(tk.END, f'Please enter a name...it is required')
        GUI.chatroom.config(state=tk.DISABLED)

    threading.Thread(target=listen_to_server, args=(client_socket, )).start()

    GUI.user_text.config(state=tk.DISABLED)
    GUI.join_button.config(state=tk.DISABLED)

    send_to_server()


class GUI:  # GUI was created with help from the Tkinter documentation (specific functions)
    root = tkb.Window()     # Tkinter/Tkbootstrap (Simply automatically does it through tkb which reformat it)
    root.geometry('750x600')  # Doc website: https://docs.python.org/3/library/tkinter.html
    root.title('Mock Messenger')
    root.resizable(False, False)
    terminal = "Terminal"
    modern = "Modern"

    label_box = tk.Frame(root, width=750, height=60)
    label_box.grid(row=0, column=0, sticky=tk.NSEW)

    app_name = tk.Label(label_box, text="Mock Messenger:", font=terminal)
    app_authors = tk.Label(label_box, text="Created by Nacim Osman/Lawrence Jones", font=modern)
    app_name.pack(side=tk.LEFT, padx=0)
    app_authors.pack(side=tk.LEFT, padx=0)

    chat_box = tk.Frame(root, width=600, height=300)
    chat_box.grid(row=1, column=0, sticky=tk.NSEW)

    user_box = tk.Frame(root, width=600, height=300)
    user_box.grid(row=2, column=0, sticky=tk.NSEW)

    user_label = tk.Label(user_box, text="Your Username:", font=terminal)
    user_label.pack(side=tk.LEFT, padx=10)

    user_text = tk.Entry(user_box, font=terminal, width=23)
    user_text.pack(side=tk.LEFT)

    join_button = tk.Button(user_box, text="Join", font=terminal,
                            command=lambda: client_to_server(client_socket))
    join_button.pack(side=tk.LEFT, padx=15)

    msg_frame = tk.Frame(root, width=600, height=300,)
    msg_frame.grid(row=4, column=0, sticky=tk.NSEW)
    msg_text = tk.Entry(msg_frame, font=terminal, width=38)
    msg_text.pack(side=tk.LEFT, padx=10)

    msg_label = tk.Label(msg_frame, text="Enter message:", font=terminal)

    send_button = tk.Button(msg_frame, text="Send", font=terminal,
                            command=send_to_server)
    send_button.pack(side=tk.LEFT, padx=10)

    exit_button = tk.Button(msg_frame, text="Exit", font=terminal,
                            command=exit_app)
    exit_button.pack(side=tk.BOTTOM, padx=10)

    chatroom = scrolledtext.ScrolledText(chat_box, font=terminal, width=55, height=25)
    chatroom.config(state=tk.DISABLED)
    chatroom.pack(side=tk.TOP)


def client():
    try:
        client_socket.connect((host, port))
        print('Client connection to server is successful')
        GUI.chatroom.config(state=tk.NORMAL)
        GUI.chatroom.insert(tk.END, 'Client connected' + '\n')
        GUI.chatroom.config(state=tk.DISABLED)
    except():
        GUI.chatroom.config(state=tk.NORMAL)
        GUI.chatroom.insert(tk.END, f'Client has failed to connect...close application and try again')
        GUI.chatroom.config(state=tk.DISABLED)


client()


GUI.root.mainloop()

