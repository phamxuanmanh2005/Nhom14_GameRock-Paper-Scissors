
Rock-Paper-Scissors (2-player pair) - Package

Files:
- server.py : server (pairing 2 players)
- client.py : GUI client (Tkinter) with sound effects
- game_logic.py : win/draw/lose logic
- assets/ : rock.png, paper.png, scissors.png, win.wav, lose.wav, draw.wav

How to run (Windows):
1. Install Python 3.8+
2. (Optional) Install playsound for audio fallback: pip install playsound==1.2.2
3. Open Terminal and run server:
   python server.py
4. Open two more Terminals and run client in each:
   python client.py
5. Enter names, click Rock/Paper/Scissors. Results will be shown and sounds played.

Notes:
- The client attempts to use winsound on Windows; if not available it tries playsound.
- Make sure firewall allows local connections on port 12345.
