import os
import random
from uuid import uuid4
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket


class Player:
    def __init__(self, username: str, character: str, decoration: str, websocket: WebSocket):
        self.username = username
        self.character = character
        self.decoration = decoration
        self.websocket = websocket
        self.id = uuid4().hex
        self.host = False


class Game:
    def __init__(self):
        self.started = False


class Room:
    def __init__(self):
        self.players: list[Player] = []
        self.game = Game()


rooms = {}


async def create_room(request: Request):
    room_id = random.randint(1000, 9999)

    rooms[room_id] = Room()

    return JSONResponse({"room_id": room_id})


async def game_ws(websocket: WebSocket):
    user_data = await websocket.receive_json()

    room: Room = rooms.get(user_data["room_id"])

    if room is None:
        await websocket.close()

    player = Player(user_data["username"], user_data["character"], user_data["decoration"], websocket)

    if len(room.players) == 0:
        player.host = True

    room.players.append(player)

    for _player in room.players:
        await _player.websocket.send_json({
            "type": "new_player_joined",
            "player_id": player.id
        })

    if player.host:
        start_game = await websocket.receive_json()


app = Starlette(debug=True, routes=[
    Mount("/", app=StaticFiles(directory="client", html=True), name="client"),
    Route("/create-room", create_room, methods=["POST"]),
    WebSocketRoute("/game", game_ws)
])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
