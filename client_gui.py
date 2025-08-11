import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import json
from PIL import Image, ImageTk  # Thêm dòng này

class RockPaperScissorsClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Kéo Búa Lá Online")
        self.root.geometry("400x450")
        
        # Kết nối mạng
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 65432
        
        # Giao diện
        self.setup_ui()
        self.connect_to_server()
    
    def setup_ui(self):
        # Frame chính
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Thông tin người chơi
        self.player_info = tk.Label(
            self.main_frame,
            text="Đang kết nối...",
            font=("Arial", 12, "bold")
        )
        self.player_info.pack(pady=10)
        
        # Trạng thái game
        self.game_status = tk.Label(
            self.main_frame,
            text="Chờ kết nối server...",
            fg="blue",
            font=("Arial", 10)
        )
        self.game_status.pack(pady=5)
        
        # Frame lựa chọn
        self.choice_frame = tk.Frame(self.main_frame)
        self.choice_frame.pack(pady=20)
        
        # Load ảnh sticker từ thư mục anh/
        self.img_keo = ImageTk.PhotoImage(Image.open("anh/keo.jpg").resize((64, 64)))
        self.img_bua = ImageTk.PhotoImage(Image.open("anh/bua.jpg").resize((64, 64)))
        self.img_la  = ImageTk.PhotoImage(Image.open("anh/la.jpg").resize((64, 64)))
        
        # Nút lựa chọn bằng ảnh
        self.buttons = []
        btn_keo = tk.Button(
            self.choice_frame,
            image=self.img_keo,
            state=tk.DISABLED,
            command=lambda: self.send_choice("kéo")
        )
        btn_keo.pack(side=tk.LEFT, padx=5)
        self.buttons.append(btn_keo)

        btn_bua = tk.Button(
            self.choice_frame,
            image=self.img_bua,
            state=tk.DISABLED,
            command=lambda: self.send_choice("búa")
        )
        btn_bua.pack(side=tk.LEFT, padx=5)
        self.buttons.append(btn_bua)

        btn_la = tk.Button(
            self.choice_frame,
            image=self.img_la,
            state=tk.DISABLED,
            command=lambda: self.send_choice("lá")
        )
        btn_la.pack(side=tk.LEFT, padx=5)
        self.buttons.append(btn_la)
        
        # Bảng điểm
        self.score_label = tk.Label(
            self.main_frame,
            text="Thắng: 0 | Thua: 0 | Hòa: 0",
            font=("Arial", 10)
        )
        self.score_label.pack(pady=15)
        
        # Chat box (mở rộng)
        self.chat_frame = tk.Frame(self.main_frame)
        self.chat_frame.pack(fill=tk.X, pady=10)
        
        self.chat_entry = tk.Entry(self.chat_frame)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(
            self.chat_frame,
            text="Gửi",
            command=self.send_chat
        ).pack(side=tk.RIGHT)
        
        # Nút thoát
        tk.Button(
            self.main_frame,
            text="Thoát Game",
            command=self.quit_game,
            bg="red",
            fg="white"
        ).pack(pady=10)
# ...giữ nguyên các hàm còn lại...import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import json
from PIL import Image, ImageTk

class RockPaperScissorsClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Kéo Búa Lá Online")
        self.root.geometry("400x450")
        
        # Kết nối mạng
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 65432
        
        # Giao diện
        self.setup_ui()
        self.connect_to_server()
    
    def setup_ui(self):
        # Frame chính
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Thông tin người chơi
        self.player_info = tk.Label(
            self.main_frame,
            text="Đang kết nối...",
            font=("Arial", 12, "bold")
        )
        self.player_info.pack(pady=10)
        
        # Trạng thái game
        self.game_status = tk.Label(
            self.main_frame,
            text="Chờ kết nối server...",
            fg="blue",
            font=("Arial", 10)
        )
        self.game_status.pack(pady=5)
        
        # Frame lựa chọn
        self.choice_frame = tk.Frame(self.main_frame)
        self.choice_frame.pack(pady=20)
        
        # Load ảnh sticker từ thư mục anh/
        self.img_keo = ImageTk.PhotoImage(Image.open("anh/keo.jpg").resize((64, 64)))
        self.img_bua = ImageTk.PhotoImage(Image.open("anh/bua.jpg").resize((64, 64)))
        self.img_la  = ImageTk.PhotoImage(Image.open("anh/la.jpg").resize((64, 64)))
        
        # Nút lựa chọn bằng ảnh
        self.buttons = []
        btn_keo = tk.Button(
            self.choice_frame,
            image=self.img_keo,
            state=tk.DISABLED,
            command=lambda: self.send_choice("kéo")
        )
        btn_keo.pack(side=tk.LEFT, padx=5)
        self.buttons.append(btn_keo)

        btn_bua = tk.Button(
            self.choice_frame,
            image=self.img_bua,
            state=tk.DISABLED,
            command=lambda: self.send_choice("búa")
        )
        btn_bua.pack(side=tk.LEFT, padx=5)
        self.buttons.append(btn_bua)

        btn_la = tk.Button(
            self.choice_frame,
            image=self.img_la,
            state=tk.DISABLED,
            command=lambda: self.send_choice("lá")
        )
        btn_la.pack(side=tk.LEFT, padx=5)
        self.buttons.append(btn_la)
        
        # Bảng điểm
        self.score_label = tk.Label(
            self.main_frame,
            text="Thắng: 0 | Thua: 0 | Hòa: 0",
            font=("Arial", 10)
        )
        self.score_label.pack(pady=15)
        
        # Nút thoát
        tk.Button(
            self.main_frame,
            text="Thoát Game",
            command=self.quit_game,
            bg="red",
            fg="white"
        ).pack(pady=10)
    
    def connect_to_server(self):
        try:
            self.socket.connect((self.host, self.port))
            
            # Nhận yêu cầu tên
            data = self.socket.recv(1024).decode()
            if data == "NAME_REQUEST":
                player_name = simpledialog.askstring("Tên người chơi",
                    "Nhập tên của bạn:",
                    parent=self.root
                ) or "Player"
                self.socket.sendall(player_name.encode())
                self.player_name = player_name
                self.player_info.config(text=f"Bạn: {player_name}")
            
            # Bắt đầu luồng nhận tin
            threading.Thread(target=self.receive_data, daemon=True).start()
            
        except ConnectionRefusedError:
            messagebox.showerror("Lỗi", "Không thể kết nối đến server!")
            self.root.quit()
    
    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(4096).decode()
                if not data:
                    break
                
                if data.startswith("WAITING|"):
                    status = data.split("|")[1]
                    self.game_status.config(text=status)
                
                elif data.startswith("GAME_START|"):
                    opponent = data.split("|")[1]
                    self.game_status.config(
                        text=f"Đang chơi với {opponent}",
                        fg="green"
                    )
                    self.enable_buttons()
                
                elif data.startswith("CHOICE_REQUEST|"):
                    prompt = data.split("|")[1]
                    self.game_status.config(text=prompt)
                    self.enable_buttons()
                
                elif data.startswith("GAME_RESULT|"):
                    result_data = json.loads(data.split("|")[1])
                    self.show_result(result_data)
                
                elif data == "PLAY_AGAIN":
                    if messagebox.askyesno("Chơi lại", "Bạn có muốn chơi lại?"):
                        self.socket.sendall("y".encode())
                        self.game_status.config(text="Chuẩn bị lượt mới...")
                    else:
                        self.socket.sendall("n".encode())
                        self.quit_game()
                
                elif data == "GAME_OVER":
                    messagebox.showinfo("Kết thúc", "Trò chơi kết thúc!")
                    self.disable_buttons()
                    self.game_status.config(text="Kết thúc game", fg="red")
            
            except (ConnectionResetError, json.JSONDecodeError):
                messagebox.showerror("Lỗi", "Mất kết nối với server!")
                self.root.quit()
                break
    
    def show_result(self, result_data):
        # Hiển thị kết quả
        p1_choice = result_data['p1_choice']
        p2_choice = result_data['p2_choice']
        result = result_data['result']
        
        if result == "p1":
            result_text = "Bạn thắng!"
        elif result == "p2":
            result_text = "Bạn thua!"
        else:
            result_text = "Hòa!"
        
        message = f"""Kết quả:
        Bạn: {p1_choice}
        Đối thủ: {p2_choice}
        {result_text}
        """
        messagebox.showinfo("Kết quả", message)
        
        # Cập nhật điểm
        scores = result_data['scores'][self.player_name]
        self.score_label.config(
            text=f"Thắng: {scores['wins']} | Thua: {scores['losses']} | Hòa: {scores['draws']}"
        )
    
    def send_choice(self, choice):
        self.socket.sendall(choice.encode())
        self.disable_buttons()
        self.game_status.config(text=f"Đã chọn: {choice}. Chờ đối thủ...")
    
    def enable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)
    
    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
    
    def quit_game(self):
        try:
            self.socket.close()
        except:
            pass
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsClient(root)
    root.mainloop()