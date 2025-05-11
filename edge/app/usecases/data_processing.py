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
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    road_state = "good" if 15000 > agent_data.accelerometer.z > 0 \
        else "bad" if agent_data.accelerometer.z < 17000 or agent_data.accelerometer.z > -1000 \
        else "very bad"
    return ProcessedAgentData(road_state=road_state, agent_data=agent_data)
