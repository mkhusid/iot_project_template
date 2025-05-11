from pydantic import BaseModel


class GpsSchema(BaseModel):
    ''' GPS data schema. '''
    latitude: float
    longitude: float
