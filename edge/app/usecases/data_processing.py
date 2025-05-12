from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData):
        Processed data containing the classified state of the road surface and agent data.
    """
    if 0 < agent_data.accelerometer.z < 15000:
        road_state = "good"
    elif -1000 < agent_data.accelerometer.z < 17000:
        road_state = "bump"
    else:
        road_state = "pothole"
    return ProcessedAgentData(road_state=road_state, agent_data=agent_data)
