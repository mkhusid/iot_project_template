from schema.accelerometer_schema import AccelerometerSchema
from schema.gps_schema import GpsSchema
from pydantic import BaseModel


class AggregatedDataSchema(BaseModel):
    ''' Aggregated data schema. '''
    accelerometer: AccelerometerSchema
    gps: GpsSchema
    timestamp: str
    user_id: int
