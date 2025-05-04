from typing import List
from fastapi import APIRouter
from src.models import ProcessedAgentDataModel
from src.database.core import session
from src.database.models import ProcessedAgentData
import src.utils.socket as socket

store_router = APIRouter()


@store_router.post("/")
async def create_processed_agent_data(data: List[ProcessedAgentDataModel]):
    session.bulk_save_objects(
        [ProcessedAgentData(
            road_state=a_data.road_state,
            user_id=a_data.agent_data.user_id,
            x=a_data.agent_data.accelerometer.x,
            y=a_data.agent_data.accelerometer.y,
            z=a_data.agent_data.accelerometer.z,
            latitude=a_data.agent_data.gps.latitude,
            longitude=a_data.agent_data.gps.longitude,
            timestamp=a_data.agent_data.timestamp
        ) for a_data in data]
    )
    try:
        await socket.send_data(data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error sending data to subscribers: {e}")
    return


@store_router.get("/{processed_agent_data_id}")
def read_processed_agent_data(processed_agent_data_id: int):
    return session.query(ProcessedAgentData).get(processed_agent_data_id)


@store_router.get("/")
def list_processed_agent_data():
    return list(session.query(ProcessedAgentData).all())


@store_router.put("/{processed_agent_data_id}")
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentDataModel):
    updated_instance = ProcessedAgentData(
        road_state=data.road_state,
        user_id=data.agent_data.user_id,
        x=data.agent_data.accelerometer.x,
        y=data.agent_data.accelerometer.y,
        z=data.agent_data.accelerometer.z,
        latitude=data.agent_data.gps.latitude,
        longitude=data.agent_data.gps.longitude,
        timestamp=data.agent_data.timestamp,
        id=processed_agent_data_id
    )

    session.merge(updated_instance)
    session.commit()
    return updated_instance


@store_router.delete("/{processed_agent_data_id}")
def delete_processed_agent_data(processed_agent_data_id: int):
    obj = session.query(ProcessedAgentData).get(processed_agent_data_id)
    session.delete(obj)
    session.commit()
    return obj


@store_router.delete("/")
def clear_all_data():
    data = session.query(ProcessedAgentData)
    lines_count = data.count()
    data.delete()
    session.commit()
    return {"lines_deleted": lines_count}
