from sqlalchemy.orm import Session
from app.core.repositories.device_repository import DeviceRepository
from app.core.schemas.device import DeviceCreate, DeviceUpdate
from uuid import UUID


class DeviceService:
    def __init__(self, db: Session):
        self.repo = DeviceRepository(db)

    def get_device(self, device_id: UUID):
        return self.repo.get(device_id)

    def get_devices(self):
        return self.repo.get_all()

    def create_device(self, device: DeviceCreate):
        return self.repo.create(device)

    def update_device(self, device_id: UUID, device: DeviceUpdate):
        return self.repo.update(device_id, device)

    def delete_device(self, device_id: UUID):
        return self.repo.delete(device_id)
