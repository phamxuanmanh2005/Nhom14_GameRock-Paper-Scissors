# server.py
import socket
import threading
from game_logic import determine_winner

HOST = "0.0.0.0"
PORT = 12345

clients = []          # list of (conn, name)
choices = {}          # conn -> choice
replay_requests = set() # set of connections that want to replay
lock = threading.Lock()

def send_safe(conn, msg):
    try:
        conn.send(msg.encode())
    except:
        pass

def handle_client(conn, addr):
    name = None
    try:
        name = conn.recv(1024).decode().strip()
        if not name:
            conn.close()
            return
        with lock:
            clients.append((conn, name))
        print(f"[JOIN] {name} from {addr}")

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            with lock:
                # Xử lý yêu cầu chơi lại
                if data == "REPLAY":
                    replay_requests.add(conn)
                    print(f"{name} đã yêu cầu chơi lại. Số yêu cầu hiện tại: {len(replay_requests)}")
                    
                    if len(replay_requests) >= 2 and len(clients) >= 2:
                        conns_to_replay = list(replay_requests)[:2]
                        for c in conns_to_replay:
                            send_safe(c, "VÁN_MỚI")
                        replay_requests.clear()
                    continue

                # Lưu lựa chọn
                choices[conn] = data
                # Nếu có hai người chơi đã chọn, tính toán và gửi kết quả cho cả hai
                if len(choices) >= 2:
                    conns = list(choices.keys())[:2]
                    c1, c2 = conns[0], conns[1]
                    n1 = next((n for (cx, n) in clients if cx == c1), "P1")
                    n2 = next((n for (cx, n) in clients if cx == c2), "P2")
                    ch1 = choices.get(c1, "")
                    ch2 = choices.get(c2, "")
                    res1 = determine_winner(ch1, ch2)
                    res2 = determine_winner(ch2, ch1)
                    
                    if res1 == "win":
                        msg1 = f"KẾT_QUẢ::{n1} ({ch1}) vs {n2} ({ch2}) → {n1} WIN 🎉"
                        msg2 = f"KẾT_QUẢ::{n1} ({ch1}) vs {n2} ({ch2}) → {n1} WIN 🎉"
                    elif res1 == "lose":
                        msg1 = f"KẾT_QUẢ::{n1} ({ch1}) vs {n2} ({ch2}) → {n2} WIN 🎉"
                        msg2 = f"KẾT_QUẢ::{n1} ({ch1}) vs {n2} ({ch2}) → {n2} WIN 🎉"
                    else:
                        msg1 = f"KẾT_QUẢ::{n1} ({ch1}) vs {n2} ({ch2}) → DRAW 🤝"
                        msg2 = msg1
                    
                    send_safe(c1, msg1)
                    send_safe(c2, msg2)
                    
                    choices.pop(c1, None)
                    choices.pop(c2, None)
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        with lock:
            clients[:] = [(c,n) for (c,n) in clients if c != conn]
            choices.pop(conn, None)
            if conn in replay_requests:
                replay_requests.remove(conn)
        try:
            conn.close()
        except:
            pass
        print(f"[DISCONNECT] {addr} ({name})")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Đang lắng nghe trên {HOST}:{PORT} (ghép đôi 2 người chơi)")
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    finally:
        server.close()

if __name__ == "__main__":
    main()
