import asyncio
import websockets
import json

waiting_player = None  # Waiting player (ws, name)
games = {}  # Matches: {ws: opponent_ws}
moves = {}  # Moves: {ws: "Rock"/"Paper"/"Scissors"}

def check_winner(move1, move2):
    """Return 0 if draw, 1 if player1 wins, 2 if player2 wins"""
    if move1 == move2:
        return 0
    rules = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }
    return 1 if rules[move1] == move2 else 2

async def handler(ws):
    global waiting_player, games, moves
    print("New player connected:", ws.remote_address)

    try:
        async for msg in ws:
            data = json.loads(msg)

            if data["action"] == "join":
                name = data["name"]
                if waiting_player is None:
                    waiting_player = (ws, name)
                    await ws.send(json.dumps({"action": "waiting"}))
                    print(f"{name} is waiting for an opponent...")
                else:
                    p1, n1 = waiting_player
                    p2, n2 = ws, name
                    games[p1] = p2
                    games[p2] = p1
                    waiting_player = None
                    print(f"Match started: {n1} vs {n2}")
                    await p1.send(json.dumps({"action": "start_game", "opponent": n2}))
                    await p2.send(json.dumps({"action": "start_game", "opponent": n1}))

            elif data["action"] == "move":
                moves[ws] = data["move"]
                opponent_ws = games.get(ws)

                if opponent_ws in moves:
                    p1_move = moves[ws]
                    p2_move = moves[opponent_ws]

                    result = check_winner(p1_move, p2_move)

                    if result == 0:
                        await ws.send(json.dumps({"action": "round_result", "message": f"Draw! ({p1_move} vs {p2_move})"}))
                        await opponent_ws.send(json.dumps({"action": "round_result", "message": f"Draw! ({p2_move} vs {p1_move})"}))
                    elif result == 1:
                        await ws.send(json.dumps({"action": "round_result", "message": f"You win! ({p1_move} vs {p2_move})"}))
                        await opponent_ws.send(json.dumps({"action": "round_result", "message": f"You lose! ({p2_move} vs {p1_move})"}))
                    else:
                        await ws.send(json.dumps({"action": "round_result", "message": f"You lose! ({p1_move} vs {p2_move})"}))
                        await opponent_ws.send(json.dumps({"action": "round_result", "message": f"You win! ({p2_move} vs {p1_move})"}))

                    del moves[ws]
                    del moves[opponent_ws]

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed: {ws.remote_address}")

    finally:
        # Clean up on disconnect
        if waiting_player and waiting_player[0] == ws:
            waiting_player = None

        opponent_ws = games.get(ws)
        if opponent_ws:
            try:
                await opponent_ws.send(json.dumps({
                    "action": "opponent_quit",
                    "message": "Your opponent has left the game."
                }))
            except:
                pass
            del games[ws]
            del games[opponent_ws]

        moves.pop(ws, None)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running at ws://127.0.0.1:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
