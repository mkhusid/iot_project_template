from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json


# WebSocket subscribers
subscribers: Dict[int, Set[WebSocket]] = {}


async def open_websocket(websocket: WebSocket, user_id: int):
    '''WebSocket endpoint for subscribing to user data.
    Args:
        websocket (WebSocket): The WebSocket connection.
        user_id (int): The user ID to subscribe to.
    '''
    print("WebSocket connection opened")
    await websocket.accept()
    if user_id not in subscribers:
        subscribers[user_id] = set()
    subscribers[user_id].add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscribers[user_id].remove(websocket)


async def send_data(data, user_id: int):
    '''Send data to all subscribers.
    Args:
        data (dict): The data to send.
    '''
    if len(subscribers) == 0:
        raise ValueError("No subscribers connected")

    messages = []
    for websocket in subscribers[user_id]:
        task = websocket.send_json(json.dumps(data))
        messages.append(task)
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(msg) for msg in messages]
    print(f"Sent data to {len(results)} subscribers")
