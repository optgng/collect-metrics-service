from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.schemas.device import DeviceCreate, DeviceUpdate, DeviceInDB
from app.core.services.device_service import DeviceService
from app.core.database import get_db
from typing import List
from uuid import UUID
import logging

router = APIRouter()

def get_device_service(db: Session = Depends(get_db)):
    return DeviceService(db)

@router.get("/", response_model=List[DeviceInDB])
def list_devices(service: DeviceService = Depends(get_device_service)):
    try:
        return service.get_devices()
    except Exception as e:
        logging.exception("Ошибка при получении списка устройств")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{device_id}", response_model=DeviceInDB)
def get_device(device_id: UUID, service: DeviceService = Depends(get_device_service)):
    device = service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/", response_model=DeviceInDB)
def create_device(device: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    return service.create_device(device)

@router.put("/{device_id}", response_model=DeviceInDB)
def update_device(device_id: UUID, device: DeviceUpdate, service: DeviceService = Depends(get_device_service)):
    updated = service.update_device(device_id, device)
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated

@router.delete("/{device_id}", response_model=DeviceInDB)
def delete_device(device_id: UUID, service: DeviceService = Depends(get_device_service)):
    deleted = service.delete_device(device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device not found")
    return deleted
