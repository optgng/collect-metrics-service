from sqlalchemy.orm import Session
from app.core.models.device import Device
from app.core.schemas.device import DeviceCreate, DeviceUpdate
from uuid import UUID


class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, device_id: UUID):
        return self.db.query(Device).filter(Device.id == device_id).first()

    def get_all(self):
        return self.db.query(Device).all()

    def create(self, device: DeviceCreate):
        db_device = Device(**device.dict())
        self.db.add(db_device)
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def update(self, device_id: UUID, device: DeviceUpdate):
        db_device = self.get(device_id)
        if not db_device:
            return None
        for field, value in device.dict(exclude_unset=True).items():
            setattr(db_device, field, value)
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def delete(self, device_id: UUID):
        db_device = self.get(device_id)
        if not db_device:
            return None
        self.db.delete(db_device)
        self.db.commit()
        return db_device
