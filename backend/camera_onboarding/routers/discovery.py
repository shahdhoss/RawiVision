from fastapi import APIRouter, status, HTTPException, Form, Depends
from ..service.automatic_discovery import AutomaticDiscovery, OnvifOnboarding, NonOnvifOnboarding
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from ..repository.cameras import CameraRepository
from ..schemas.metadata import CameraMetadataResponse
from typing import List

camera_discovery_router = APIRouter(prefix="/camera", tags=["discover online cameras"])

async def get_camera_repository(db: AsyncSession=Depends(get_db)):
    return CameraRepository(db=db)

async def get_onvif_onboarding():
    return OnvifOnboarding()

async def get_non_onvif_onboarding():
    return NonOnvifOnboarding()

async def get_automatic_discovery(onvif_onboarding: OnvifOnboarding=Depends(get_onvif_onboarding), non_onvif_onboarding: NonOnvifOnboarding=Depends(get_non_onvif_onboarding), repo:CameraRepository = Depends(get_camera_repository)):
    return AutomaticDiscovery(repo=repo, onvif_onboarding=onvif_onboarding, non_onvif_onboarding=non_onvif_onboarding)

@camera_discovery_router.get("/discovery", response_model=List[CameraMetadataResponse], status_code=status.HTTP_200_OK)
async def get_camera_metadata(automatic_discovery: AutomaticDiscovery = Depends(get_automatic_discovery)):
    camera_metadata = await automatic_discovery.get_saved_cameras_metadata()
    return camera_metadata