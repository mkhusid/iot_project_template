''' This is the main entry point for the FastAPI application. 
It sets up the FastAPI app, includes the router, and defines the WebSocket endpoint. '''
from fastapi import FastAPI, WebSocket
from src.router import store_router
import src.utils.socket as socket
import uvicorn

# FastAPI app setup
app = FastAPI()
app.include_router(store_router, prefix='/store')


@app.websocket("/ws/")
async def open_ws(websocket: WebSocket):
    await socket.open_websocket(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
