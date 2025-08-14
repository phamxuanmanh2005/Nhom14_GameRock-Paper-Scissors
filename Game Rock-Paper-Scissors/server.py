import socket
import threading
from common import recv_json, send_json, WIN_RULES

HOST = '127.0.0.1'
PORT = 65432

clients_waiting = []
lock = threading.Lock()

def handle_match(p1, p2):
    scores = {p1: 0, p2: 0}

    while True:
        # Nhận lựa chọn
        choice1 = recv_json(p1)["choice"]
        choice2 = recv_json(p2)["choice"]

        # Xác định kết quả
        if choice1 == choice2:
            winner = 0
        elif choice2 in WIN_RULES[choice1]:
            winner = 1
            scores[p1] += 1
        else:
            winner = 2
            scores[p2] += 1

        # Gửi kết quả cho cả 2
        send_json(p1, {"your_choice": choice1, "opponent_choice": choice2,
                       "scores": scores, "winner": winner})
        send_json(p2, {"your_choice": choice2, "opponent_choice": choice1,
                       "scores": scores, "winner": winner})

        # Thắng 2/3
        if scores[p1] == 2 or scores[p2] == 2:
            send_json(p1, {"game_over": True})
            send_json(p2, {"game_over": True})
            break

def handle_client(conn):
    with lock:
        clients_waiting.append(conn)
        if len(clients_waiting) >= 2:
            p1 = clients_waiting.pop(0)
            p2 = clients_waiting.pop(0)
            threading.Thread(target=handle_match, args=(p1, p2)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server đang chạy...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    main()
