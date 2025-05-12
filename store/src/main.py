''' This is the main entry point for the FastAPI application. 
It sets up the FastAPI app, includes the router, and defines the WebSocket endpoint. '''
from fastapi import FastAPI, WebSocket
from src.router import store_router
import src.utils.socket as socket
import uvicorn


# FastAPI app setup
app = FastAPI()
app.include_router(store_router, prefix='/store', tags=['iot-store'])


@app.websocket("/ws/{user_id}")
async def open_ws(websocket: WebSocket, user_id: int):
    ''' WebSocket endpoint for handling incoming WebSocket connections. '''
    await socket.open_websocket(websocket, user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
