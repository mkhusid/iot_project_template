from typing import List
from fastapi import APIRouter
from src.schemas.agent_data_model import ProcessedAgentDataModel
from src.database.core import db_session
from src.models.processed_agent_data import ProcessedAgentData
import src.utils.socket as socket


store_router = APIRouter()


@store_router.post("/")
async def create_processed_agent_data(data: List[ProcessedAgentDataModel], session: db_session):
    processed_agent_data = [ProcessedAgentData(
        road_state=a_data.road_state,
        user_id=a_data.agent_data.user_id,
        x=a_data.agent_data.accelerometer.x,
        y=a_data.agent_data.accelerometer.y,
        z=a_data.agent_data.accelerometer.z,
        latitude=a_data.agent_data.gps.latitude,
        longitude=a_data.agent_data.gps.longitude,
    ) for a_data in data]
    session.add_all(processed_agent_data)

    try:
        await socket.send_data(data)
        await session.commit()
        return [{"id": data.id, "timestamp": data.timestamp} for data in processed_agent_data]

    except Exception as e:
        await session.rollback()
        print(f"Error sending data to subscribers: {e}")


@store_router.get("/{processed_agent_data_id}")
async def read_processed_agent_data(processed_agent_data_id: int, session: db_session):
    async with session:
        result = await ProcessedAgentData.select(session, id=processed_agent_data_id)
        return result[0] if result else {"message": "Instance not found"}


@store_router.get("/")
async def list_processed_agent_data(session: db_session):
    async with session:
        return await ProcessedAgentData.select(session)


@store_router.put("/{processed_agent_data_id}")
async def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentDataModel, session: db_session):
    async with session:
        result = await ProcessedAgentData.select(session, id=processed_agent_data_id)
        instance = result[0] if result else None
        if not instance:
            return {"message": "Instance not found"}

        instance.road_state = data.road_state
        instance.user_id = data.agent_data.user_id
        instance.x = data.agent_data.accelerometer.x
        instance.y = data.agent_data.accelerometer.y
        instance.z = data.agent_data.accelerometer.z
        instance.latitude = data.agent_data.gps.latitude
        instance.longitude = data.agent_data.gps.longitude

        await session.commit()
        return instance


@store_router.delete("/{processed_agent_data_id}")
async def delete_processed_agent_data(processed_agent_data_id: int, session: db_session):
    async with session:
        result = await ProcessedAgentData.select(session, id=processed_agent_data_id)
        instance = result[0] if result else None
        if not instance:
            return {"message": "Instance not found"}

        await session.delete(instance)
        await session.commit()
        return {"message": "Deleted successfully"}


@store_router.delete("/")
async def clear_all_data(session: db_session):
    async with session:
        instances = await ProcessedAgentData.select(session)
        for instance in instances:
            await session.delete(instance)
        await session.commit()
        return {"message": "All data cleared"}
