import socket
import random

def start_client():
    host = '127.0.0.1'
    port = 65432
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    try:
        player_name = input("Nhập tên của bạn: ").strip() or f"Player{random.randint(1, 100)}"
        client.sendall(player_name.encode())
        
        while True:
            data = client.recv(4096).decode()
            if not data:
                break
            
            if data.startswith("CHỜ|"):
                print(data.split("|")[1])
            elif data.startswith("CHỌN|"):
                choice = input(data.split("|")[1] + " ").lower()
                while choice not in ['kéo', 'búa', 'lá']:
                    print("Lựa chọn không hợp lệ! Chọn lại.")
                    choice = input(data.split("|")[1] + " ").lower()
                client.sendall(choice.encode())
            elif data.startswith("KẾT QUẢ|"):
                print("\n" + data.split("|")[1])
            elif data.startswith("CHƠI LẠI|"):
                choice = input(data.split("|")[1] + " ").lower()
                while choice not in ['y', 'n']:
                    print("Vui lòng nhập y (có) hoặc n (không)")
                    choice = input(data.split("|")[1] + " ").lower()
                client.sendall(choice.encode())
                if choice == 'n':
                    break
            else:
                print(data)
                
    except (ConnectionResetError, BrokenPipeError):
        print("\nMất kết nối với server!")
    finally:
        client.close()
        print("Đã thoát game.")

if __name__ == "__main__":
    start_client()