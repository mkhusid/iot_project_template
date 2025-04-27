''' This is the main entry point for the FastAPI application. 
It sets up the FastAPI app, includes the router, and defines the WebSocket endpoint. '''
from fastapi import FastAPI, WebSocket
from router import store_router
import store.utils.socket as socket

# FastAPI app setup
app = FastAPI()
app.include_router(store_router, prefix='/store')


@app.websocket("/ws/{user_id}")
async def open_ws(websocket: WebSocket, user_id: int):
    await socket.open_websocket(websocket, user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
