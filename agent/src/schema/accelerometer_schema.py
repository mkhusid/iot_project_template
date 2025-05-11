from pydantic import BaseModel

class AccelerometerSchema(BaseModel):
    ''' Accelerometer data schema. '''
    x: float
    y: float
    z: float
