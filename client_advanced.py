import socket
import json

class RockPaperScissorsCLI:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 65432
        self.player_name = None
    
    def start(self):
        try:
            # Kết nối server
            self.socket.connect((self.host, self.port))
            print("Đã kết nối đến server...")
            
            # Nhập tên
            data = self.socket.recv(1024).decode()
            if data == "NAME_REQUEST":
                self.player_name = input("Nhập tên của bạn: ").strip() or "Player"
                self.socket.sendall(self.player_name.encode())
                print(f"Xin chào {self.player_name}! Đang tìm đối thủ...")
            
            # Nhận tin nhắn
            while True:
                data = self.socket.recv(4096).decode()
                if not data:
                    break
                
                if data.startswith("WAITING|"):
                    print(data.split("|")[1])
                
                elif data.startswith("GAME_START|"):
                    print("\n" + data.split("|")[1] + "\n")
                
                elif data.startswith("CHOICE_REQUEST|"):
                    choice = input(data.split("|")[1] + ": ").lower()
                    while choice not in ['kéo', 'búa', 'lá']:
                        print("Lựa chọn không hợp lệ!")
                        choice = input(data.split("|")[1] + ": ").lower()
                    self.socket.sendall(choice.encode())
                
                elif data.startswith("GAME_RESULT|"):
                    result = json.loads(data.split("|")[1])
                    self.show_result(result)
                
                elif data == "PLAY_AGAIN":
                    choice = input("Chơi lại? (y/n): ").lower()
                    while choice not in ['y', 'n']:
                        choice = input("Chơi lại? (y/n): ").lower()
                    self.socket.sendall(choice.encode())
                    if choice == 'n':
                        break
                
                elif data == "GAME_OVER":
                    print("\nTrò chơi kết thúc!")
                    break
            
        except ConnectionRefusedError:
            print("Không thể kết nối đến server!")
        except (ConnectionResetError, BrokenPipeError):
            print("\nMất kết nối với server!")
        finally:
            self.socket.close()
    
    def show_result(self, result_data):
        print("\n=== KẾT QUẢ ===")
        print(f"Bạn: {result_data['p1_choice']}")
        print(f"Đối thủ: {result_data['p2_choice']}")
        
        if result_data['result'] == "p1":
            print("Bạn thắng!")
        elif result_data['result'] == "p2":
            print("Bạn thua!")
        else:
            print("Hòa!")
        
        stats = result_data['scores'][self.player_name]
        print(f"\nThống kê:")
        print(f"- Thắng: {stats['wins']}")
        print(f"- Thua: {stats['losses']}")
        print(f"- Hòa: {stats['draws']}")
        print("===============\n")

if __name__ == "__main__":
    client = RockPaperScissorsCLI()
    client.start()