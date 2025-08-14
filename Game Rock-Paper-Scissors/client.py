import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

HOST = '127.0.0.1'
PORT = 65432

class RPSClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Kéo – Búa – Bao (Nhóm 14)")
        self.root.geometry("500x400")
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.choice = None
        self.round_wins = 0
        self.opponent_wins = 0

        self.build_ui()

        # Thread nhận dữ liệu từ server
        threading.Thread(target=self.receive_data, daemon=True).start()

    def build_ui(self):
        tk.Label(self.root, text="Chọn của bạn:", font=("Arial", 14)).pack(pady=10)

        frame_choices = tk.Frame(self.root)
        frame_choices.pack()

        self.buttons = {}
        for choice in ["rock", "paper", "scissors"]:
            img = Image.open(f"{choice}.png").resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            btn = tk.Button(frame_choices, image=photo, command=lambda c=choice: self.send_choice(c))
            btn.image = photo  # giữ tham chiếu
            btn.pack(side=tk.LEFT, padx=10)
            self.buttons[choice] = btn

        self.label_status = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_status.pack(pady=20)

        self.label_score = tk.Label(self.root, text="Bạn: 0 | Đối thủ: 0", font=("Arial", 12))
        self.label_score.pack(pady=10)

    def send_choice(self, choice):
        if self.choice is None:
            self.choice = choice
            self.sock.sendall(choice.encode())
            self.label_status.config(text=f"Bạn đã chọn: {choice}")

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                if data.startswith("RESULT:"):
                    result = data.split(":")[1]
                    self.process_result(result)
                else:
                    self.label_status.config(text=data)
            except:
                break

    def process_result(self, result):
        if result == "WIN":
            self.round_wins += 1
        elif result == "LOSE":
            self.opponent_wins += 1

        self.label_score.config(text=f"Bạn: {self.round_wins} | Đối thủ: {self.opponent_wins}")
        self.choice = None

        if self.round_wins == 2:
            messagebox.showinfo("Kết quả", "🎉 Bạn thắng trận này!")
            self.reset_score()
        elif self.opponent_wins == 2:
            messagebox.showinfo("Kết quả", "😢 Bạn thua trận này!")
            self.reset_score()

    def reset_score(self):
        self.round_wins = 0
        self.opponent_wins = 0
        self.label_score.config(text="Bạn: 0 | Đối thủ: 0")

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSClient(root)
    root.mainloop()
