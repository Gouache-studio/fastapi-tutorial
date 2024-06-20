from pydantic import BaseModel

class ClientDashboard(BaseModel):
    name       : str
    description: str