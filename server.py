import socket
import threading

clients = []
lock = threading.Lock()

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"[RECEIVED] {addr} -> {data}")
            with lock:
                for c in clients:
                    if c != client_socket:
                        c.send(data.encode())
    except:
        print(f"[DISCONNECTED] {addr}")
    finally:
        with lock:
            clients.remove(client_socket)
        client_socket.close()

def main():
    host = '0.0.0.0'
    port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[LISTENING] Server is running on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        with lock:
            clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    main()
