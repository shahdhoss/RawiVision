from fastapi import Depends, APIRouter, status, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from ..service.ingestion import IngestionService
from camera_onboarding.service.metadata import CameraMetadataService
from camera_onboarding.repository.camera_metdata import CameraMetadataRepository

ingestion_router = APIRouter(prefix="/ingestion", tags=["manage online cameras ingestion"])

async def get_metadata_repository(db: AsyncSession=Depends(get_db)):
    return CameraMetadataRepository(db=db)

async def get_metadata_service(repo: CameraMetadataRepository=Depends(get_metadata_repository)):
    return CameraMetadataService(repository=repo)

async def get_ingestion_service(metadata_service: CameraMetadataService=Depends(get_metadata_service)):
    return IngestionService(service=metadata_service)

@ingestion_router.get("", status_code=status.HTTP_200_OK)
async def start_ingestion(service: IngestionService = Depends(get_ingestion_service)):
    await service.start_ingestion()

