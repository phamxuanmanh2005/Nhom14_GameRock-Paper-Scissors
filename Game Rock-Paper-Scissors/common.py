import json

CHOICES = ["rock", "paper", "scissors"]
WIN_RULES = {
    "rock": ["scissors"],
    "paper": ["rock"],
    "scissors": ["paper"]
}

def send_json(sock, data):
    sock.sendall(json.dumps(data).encode())

def recv_json(sock):
    try:
        data = sock.recv(4096)
        if not data:
            return None
        return json.loads(data.decode())
    except:
        return None

# Test logic
if __name__ == "__main__":
    assert "scissors" in WIN_RULES["rock"]
    assert "rock" in WIN_RULES["paper"]
    assert "paper" in WIN_RULES["scissors"]
    print("Logic test OK")
