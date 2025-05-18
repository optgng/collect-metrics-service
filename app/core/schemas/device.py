from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DeviceBase(BaseModel):
    name: str
    description: Optional[str] = None
    ip_address: str
    system_name: Optional[str] = None  # новое поле

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class DeviceInDB(DeviceBase):
    id: UUID

    class Config:
        from_attributes = True

__all__ = [
    "DeviceBase",
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceInDB",
]
