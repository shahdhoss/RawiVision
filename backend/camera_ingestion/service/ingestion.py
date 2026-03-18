from camera_onboarding.service.metadata import CameraMetadataService
from ..celery_tasks.ingestion import capture_rtsp_video

class IngestionService:
    def __init__(self, service: CameraMetadataService):
        self.service = service
    
    async def get_online_cameras(self):
        cameras = await self.service.get_all_camera_metadata() # calling this instead of the sync function beacuse this one takes less time for running
        return cameras

    async def start_ingestion(self, duration=120):
        cameras = await self.get_online_cameras()
        if not cameras:
            raise "No online cameras"
        for camera in cameras:
            rtsp_urls = camera.rtsp_urls
            capture_rtsp_video.delay(rtsp_urls, camera.mac_address, duration=30)


