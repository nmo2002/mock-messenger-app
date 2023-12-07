import socket
import threading
import ssl

# server
# SOURCES USED TO:
# THE SOURCES GIVEN IN THE PROJECT INSTRUCTION DOCUMENT...such as the BOGOTOGO.COM and TLS wrapping
# https://www.youtube.com/watch?v=A_Z1lgZLSNc TO UNDERSTAND THREADING...
# https://www.youtube.com/watch?v=bguFKIgEpoM to install openssl
# https://www.youtube.com/watch?v=ibf5cx221hk tkinter introduction video
# https://docs.python.org/3/library/tkinter.html tkinter documentation
# https://snyk.io/blog/implementing-tls-ssl-python/  implement tls steps to understanding...

# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain(certfile="servcert.pem", keyfile="serv.pem")
# context.load_verify_locations(cafile="servcert.pem")

# I REALLY TRIED TO GET TLS TO WORK BUT COULDN'T FIGURE OUT. I UNDERSTAND THE USE OF THE WRAPPER BUT KEPT SAYING
# SOME FUNCTIONS WERE DEPRECATED....

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 3351
users = []
# server_socket = context.wrap_socket(server_socket, do_handshake_on_connect=True)


def forward(message):
    for user in users:
        user[1].sendall(message.encode())


def listener_client(client, user):
    while True:
        try:
            response = client.recv(2048).decode('utf-8')
        except ConnectionResetError:
            print(f'{user} has left the server...')
            users.remove([user, client])
            break
        if response != "":
            if response == '.exit':
                print(f"{user} exited chat")
                users.remove([user, client])
                break
            message = f'{user}-> {response}'
            forward(message)
        else:
            print(f'Empty message from {user}')
            break


def add_users(client):
    while True:
        try:
            user = client.recv(2048).decode('utf-8')
        except():
            break
        if user != "":
            users.append([user, client])
            print(f"New list of active users: ")
            for i in range(len(users)):
                print({users[i][0]})
            break
    threading.Thread(target=listener_client, args=(client, user, )).start()


def server():
    try:
        server_socket.bind((host, port))
        print(f'Server has been established...\nServer host: {host}\nServer port: {port}')
    except():
        print('[ERROR]: Unable to run server...check host and port')
    server_socket.listen(5)


server()

try:
    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=add_users, args=(client_socket, )).start()
        print(f'New entity {address} has connected to the server')
finally:
    close_server_socket = 'No'
    while close_server_socket != 'Yes':
        close_server_socket = input("Do you want to shutdown the server? (Yes or No): ")
        if close_server_socket == 'Yes':
            server_socket.close()
            exit(0)
