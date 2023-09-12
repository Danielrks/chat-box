import socket
import threading

ip = "127.0.0.1"
port = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, port))
server_socket.listen(5)

clients = []
nicknames = []


def broadcast(msg):
    for client in clients:
        client.send(msg)


def handling(client):
    while True:
        try:
            msg = client.recv(1024)

            broadcast(f"{nickname}:{msg}".encode("utf-8"))
        except:
            nickname_index = clients.index(client)
            client.close()
            broadcast(f"{nickname_index} left the chat".encode("utf-8"))
            clients.remove(client)
            nicknames.remove(nickname_index)
            break


def managing():
    global nickname
    while True:
        client, address = server_socket.accept()
        print(f"connection successfully established with {address}")
        clients.append(client)
        client.send("requesting...nickname...please...enter...your...nickname".encode("utf-8"))
        nickname = client.recv(1024)
        broadcast(f"{nickname} has joined the chat".encode("utf-8"))
        print(nickname)
        nicknames.append(nickname)
        handling_thread = threading.Thread(target=handling, args=(client, ))
        handling_thread.start()


managing()
