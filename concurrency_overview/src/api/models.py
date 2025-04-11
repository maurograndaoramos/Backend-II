from pydantic import BaseModel

class RawData(BaseModel):
    """
    Model for raw data input.
    """
    _id: str
    id: int
    uuid: str
    firstname: str
    lastname: str
    username: str
    password: str
    email: str
    ip: str
    macAddress: str
    website: str
    image: str


class ProcessedData(BaseModel):
    """
    Model for processed data input.
    """
    firstname: str
    lastname: str
    email: str
