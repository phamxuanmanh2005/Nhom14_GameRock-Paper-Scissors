# Nhom14_GameRock-Paper-Scissors
## Giới thiệu
Dự án **Kéo – Búa – Lá** nhiều người chơi, được viết bằng Python với giao tiếp **TCP socket**.  
Có thể chơi bằng **giao diện đồ họa (GUI)** hoặc **dòng lệnh (Terminal)**.  
Server sẽ tự động ghép cặp người chơi và thống kê số trận **Thắng / Thua / Hòa**.

## Tính năng
- Chơi **1 vs 1** qua mạng LAN hoặc trên cùng máy.
- 2 chế độ client:
  - **client_gui.py** – Giao diện Tkinter.
  - **client_advance.py** – Chạy trong terminal.
- Giới hạn thời gian 30 giây cho mỗi lượt chơi.
- Thống kê kết quả sau mỗi ván.
- Xử lý mất kết nối và thoát game.
