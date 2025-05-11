from typing import Set
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json


# WebSocket subscribers
subscribers: Set[WebSocket] = set()


async def open_websocket(websocket: WebSocket):
    '''WebSocket endpoint for subscribing to user data.
    Args:
        websocket (WebSocket): The WebSocket connection.
        user_id (int): The user ID to subscribe to.
    '''
    print("WebSocket connection opened")
    await websocket.accept()
    subscribers.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        subscribers.remove(websocket)


async def send_data(data):
    '''Send data to all subscribers.
    Args:
        data (dict): The data to send.
    '''
    if len(subscribers) == 0:
        raise ValueError("No subscribers connected")

    messages = []
    for websocket in subscribers:
        task = websocket.send_json(json.dumps(data))
        messages.append(task)
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(msg) for msg in messages]
    print(f"Sent data to {len(results)} subscribers")
