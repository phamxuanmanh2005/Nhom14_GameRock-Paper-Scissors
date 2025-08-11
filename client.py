# client.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import socket, threading, os, sys, time
from PIL import Image, ImageTk

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

# Chức năng phát âm thanh, sử dụng winsound trên Windows và playsound như một fallback
def play_sound(path):
    try:
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        return
    except Exception:
        pass
    try:
        from playsound import playsound
        threading.Thread(target=playsound, args=(path,), daemon=True).start()
    except Exception as e:
        print("Không tìm thấy thư viện âm thanh:", e)

# Khởi tạo Tkinter và yêu cầu người chơi nhập tên
window = tk.Tk()
window.withdraw()
player_name = None
while not player_name:
    player_name = simpledialog.askstring("Nhập tên", "Tên người chơi:", parent=window)
    if player_name is None:
        window.destroy(); sys.exit(0)
    player_name = player_name.strip()
    if not player_name:
        messagebox.showerror("Lỗi", "Tên không được để trống.", parent=window)
        player_name = None

# Kết nối đến server, thử lại 5 lần
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
for i in range(5):
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
        connected = True
        break
    except Exception as e:
        print("Kết nối thất bại:", e)
        time.sleep(1)
if not connected:
    messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới server {SERVER_HOST}:{SERVER_PORT}", parent=window)
    window.destroy(); sys.exit(1)

# Gửi tên người chơi đến server
try:
    sock.send(player_name.encode())
except:
    pass

# Cài đặt giao diện GUI
window.title(f"RPS - {player_name}")
window.geometry("420x520")
window.configure(bg="#f0f0f0")

# Tải hình ảnh
def load_img(fname):
    p = os.path.join(os.path.dirname(__file__), "assets", fname)
    if not os.path.exists(p):
        messagebox.showerror("Thiếu tệp tin", p, parent=window); window.destroy(); sys.exit(1)
    img = Image.open(p).resize((100,100))
    return ImageTk.PhotoImage(img)
window.rock_img = load_img("rock.png")
window.paper_img = load_img("paper.png")
window.scissors_img = load_img("scissors.png")

buttons_disabled = False
def send_choice(choice):
    global buttons_disabled
    if buttons_disabled and choice not in ["rock", "paper", "scissors", "REPLAY"]:
        return
    try:
        sock.send(choice.encode())
        if choice in ["rock", "paper", "scissors"]:
            buttons_disabled = True
            disable_buttons()
        # Ẩn nút "Chơi lại" khi người chơi nhấn vào
        if choice == "REPLAY":
            play_again_btn.pack_forget()
    except Exception as e:
        messagebox.showerror("Lỗi gửi", f"{e}", parent=window)

def disable_buttons():
    rock_btn.config(state="disabled")
    paper_btn.config(state="disabled")
    scissors_btn.config(state="disabled")

def enable_buttons():
    global buttons_disabled
    buttons_disabled = False
    rock_btn.config(state="normal")
    paper_btn.config(state="normal")
    scissors_btn.config(state="normal")
    result_label.config(text="Chọn lại để bắt đầu ván mới!")
    play_again_btn.pack_forget()

def create_btn(parent, img, choice):
    b = tk.Button(parent, image=img, command=lambda: send_choice(choice), bd=0)
    b.image = img
    return b

# Luồng nhận dữ liệu từ server
def handle_recv():
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            if data.startswith("KẾT_QUẢ::"):
                msg = data.replace("KẾT_QUẢ::","")
                window.after(0, lambda m=msg: show_result_and_sound(m))
            elif data == "VÁN_MỚI":
                window.after(0, lambda: enable_buttons())
        except Exception as e:
            print("Lỗi nhận dữ liệu", e)
            break

def show_result_and_sound(msg):
    global buttons_disabled
    buttons_disabled = True
    result_label.config(text=msg)
    lower = msg.lower()
    if "win" in lower or "🎉" in msg:
        play_sound(os.path.join(os.path.dirname(__file__), "assets", "win.wav"))
    elif "draw" in lower or "🤝" in msg:
        play_sound(os.path.join(os.path.dirname(__file__), "assets", "draw.wav"))
    else:
        play_sound(os.path.join(os.path.dirname(__file__), "assets", "lose.wav"))
    
    play_again_btn.pack(pady=10)

# Xây dựng giao diện UI
tk.Label(window, text=f"Người chơi: {player_name}", bg="#f0f0f0", font=("Helvetica",12)).pack(pady=8)
tk.Label(window, text="Chọn Búa, Bao, hoặc Kéo", bg="#f0f0f0", font=("Helvetica",14)).pack(pady=6)

frame = tk.Frame(window, bg="#f0f0f0"); frame.pack(pady=10)
rock_btn = create_btn(frame, window.rock_img, "rock")
paper_btn = create_btn(frame, window.paper_img, "paper")
scissors_btn = create_btn(frame, window.scissors_img, "scissors")
rock_btn.grid(row=0, column=0, padx=12); paper_btn.grid(row=0, column=1, padx=12); scissors_btn.grid(row=0, column=2, padx=12)

result_label = tk.Label(window, text="", font=("Arial",16,"bold"), bg="#f0f0f0"); result_label.pack(pady=20)
play_again_btn = tk.Button(window, text="Chơi lại", font=("Helvetica", 12), command=lambda: send_choice("REPLAY"))

# Bắt đầu luồng nhận dữ liệu
t = threading.Thread(target=handle_recv, daemon=True); t.start()

window.deiconify()
try:
    window.mainloop()
finally:
    try: sock.close()
    except: pass
