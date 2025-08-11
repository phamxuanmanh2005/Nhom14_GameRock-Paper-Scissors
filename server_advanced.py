import socket
import threading
import time
from collections import defaultdict
import json

class RockPaperScissorsServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lock = threading.Lock()
        self.waiting_players = []
        self.active_games = {}
        self.scores = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0})
        self.player_counter = 1

    def determine_winner(self, p1_choice, p2_choice):
        if p1_choice == p2_choice:
            return "draw"
        win_conditions = {'kéo': 'lá', 'búa': 'kéo', 'lá': 'búa'}
        return "p1" if win_conditions[p1_choice] == p2_choice else "p2"

    def handle_client(self, conn, addr, player_id):
        print(f"[NEW CONNECTION] {addr} connected as Player {player_id}")
        player_name = None

        def receive_choice(player):
            try:
                while True:
                    data = player['conn'].recv(1024).decode().strip()
                    if data in ['kéo', 'búa', 'lá', 'keo', 'bua', 'la']:
                        mapping = {'keo': 'kéo', 'bua': 'búa', 'la': 'lá'}
                        if data in mapping:
                            data = mapping[data]
                        with self.lock:
                            player['choice'] = data
                            player['ready'] = True
            except Exception:
                pass

        try:
            # Nhận tên người chơi
            conn.sendall("NAME_REQUEST".encode())
            player_name = conn.recv(1024).decode().strip() or f"Player{player_id}"
            
            with self.lock:
                self.waiting_players.append({
                    'id': player_id,
                    'conn': conn,
                    'name': player_name,
                    'choice': None,
                    'ready': False
                })
            
            # Chờ ghép cặp
            conn.sendall(f"WAITING|Đang tìm đối thủ cho {player_name}...".encode())
            
            game_room = None
            while not game_room:
                with self.lock:
                    if len(self.waiting_players) >= 2:
                        game_room = {
                            'p1': self.waiting_players.pop(0),
                            'p2': self.waiting_players.pop(0),
                            'start_time': time.time()
                        }
                        self.active_games[player_id] = game_room
                time.sleep(1)
            
            # Thông báo bắt đầu game
            p1, p2 = game_room['p1'], game_room['p2']
            p1['conn'].sendall(f"GAME_START|Đối thủ: {p2['name']}".encode())
            p2['conn'].sendall(f"GAME_START|Đối thủ: {p1['name']}".encode())

            # Tạo thread nhận lựa chọn cho từng player
            t1 = threading.Thread(target=receive_choice, args=(p1,), daemon=True)
            t2 = threading.Thread(target=receive_choice, args=(p2,), daemon=True)
            t1.start()
            t2.start()
            # Game loop
            while True:
                # Reset choices
                with self.lock:
                    p1['choice'] = None
                    p2['choice'] = None
                    p1['ready'] = False
                    p2['ready'] = False
                
                # Yêu cầu chọn
                p1['conn'].sendall("CHOICE_REQUEST|Chọn kéo/búa/lá".encode())
                p2['conn'].sendall("CHOICE_REQUEST|Chọn kéo/búa/lá".encode())
                
                # Chờ cả 2 chọn
                start_time = time.time()
                while time.time() - start_time < 30:  # Timeout 30s
                    with self.lock:
                        if p1['ready'] and p2['ready']:
                            break
                    time.sleep(0.1)
                
                # Xử lý kết quả
                with self.lock:
                    result = self.determine_winner(p1['choice'], p2['choice'])

                    # Cập nhật điểm
                    if result == "p1":
                        self.scores[p1['name']]['wins'] += 1
                        self.scores[p2['name']]['losses'] += 1
                    elif result == "p2":
                        self.scores[p1['name']]['losses'] += 1
                        self.scores[p2['name']]['wins'] += 1
                    else:
                        self.scores[p1['name']]['draws'] += 1
                        self.scores[p2['name']]['draws'] += 1

                    # Gửi kết quả cho từng client với vai trò đúng
                    result_msg_p1 = {
                        'p1_choice': p1['choice'],
                        'p2_choice': p2['choice'],
                        'result': result,
                        'scores': {
                            p1['name']: self.scores[p1['name']],
                            p2['name']: self.scores[p2['name']]
                        }
                    }
                    # Đảo kết quả cho p2
                    result_for_p2 = "p1" if result == "p2" else "p2" if result == "p1" else "draw"
                    result_msg_p2 = {
                        'p1_choice': p2['choice'],
                        'p2_choice': p1['choice'],
                        'result': result_for_p2,
                        'scores': {
                            p2['name']: self.scores[p2['name']],
                            p1['name']: self.scores[p1['name']]
                        }
                    }
                    p1['conn'].sendall(f"GAME_RESULT|{json.dumps(result_msg_p1)}".encode())
                    p2['conn'].sendall(f"GAME_RESULT|{json.dumps(result_msg_p2)}".encode())
                
                # Hỏi chơi lại
                p1['conn'].sendall("PLAY_AGAIN".encode())
                p2['conn'].sendall("PLAY_AGAIN".encode())
                
                p1_response = p1['conn'].recv(1024).decode().lower()
                p2_response = p2['conn'].recv(1024).decode().lower()
                
                if p1_response != 'y' or p2_response != 'y':
                    break
            
            # Kết thúc game
            p1['conn'].sendall("GAME_OVER".encode())
            p2['conn'].sendall("GAME_OVER".encode())
            
        except (ConnectionResetError, BrokenPipeError):
            print(f"[ERROR] Player {player_name} disconnected")
        finally:
            with self.lock:
                if player_id in self.active_games:
                    del self.active_games[player_id]
                self.waiting_players = [p for p in self.waiting_players if p['id'] != player_id]
            conn.close()
            print(f"[DISCONNECTED] Player {player_name} left")

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"[SERVER] Listening on {self.host}:{self.port}")
        
        try:
            while True:
                conn, addr = self.server.accept()
                player_id = self.player_counter
                self.player_counter += 1
                thread = threading.Thread(target=self.handle_client, args=(conn, addr, player_id))
                thread.start()
        finally:
            self.server.close()

if __name__ == "__main__":
    server = RockPaperScissorsServer()
    server.start()