from .non_onvif_onboarding import NonOnvifOnboarding
from .onvif_onboarding import OnvifOnboarding
from ..repository.cameras import CameraRepository
from ..schemas.metadata import CameraMetadataResponse
import asyncio

class AutomaticDiscovery():
    def __init__(self, onvif_onboarding: OnvifOnboarding, non_onvif_onboarding: NonOnvifOnboarding, repo: CameraRepository):
        self.discovered_camera_ips=[]
        self.onvif_onboarding = onvif_onboarding
        self.non_onvif_onboarding = non_onvif_onboarding
        self.repo = repo

    async def discover_camera_ips(self):
        onvif_ips = self.onvif_onboarding.get_camera_ip_addresses() # this could be slowing down my code
        db_cameras = await self.repo.get_all_cameras()
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, lambda c=camera: self.non_onvif_onboarding.get_camera_ip_addresses(username=c.username, password=c.password)) for camera in db_cameras]
        results = await asyncio.gather(*tasks) 
        for non_onvif_ips in results:
            self.discovered_camera_ips.extend(non_onvif_ips)
        self.discovered_camera_ips.extend(onvif_ips)
        return self.discovered_camera_ips
    
    async def get_saved_cameras_metadata(self):
        try: 
            cameras_info: list[CameraMetadataResponse]=[]
            camera_ips = await self.discover_camera_ips()
            print(camera_ips)
            db_cameras = await self.repo.get_all_cameras()
            for ip in camera_ips:
                mac_address = self.onvif_onboarding.discover_mac_address(ip)
                for camera in db_cameras:
                    if camera.mac_address == mac_address:
                        info = self.onvif_onboarding.get_camera_info(ip=ip, username=camera.username, password=camera.password, mac_address=camera.mac_address)
                        camera_info_instance = CameraMetadataResponse(room=camera.room, building=camera.building, username= camera.username, password= camera.password, rtsp_urls=info["rtsp_urls"] ,ip_address=ip, mac_address= camera.mac_address)
                        cameras_info.append(camera_info_instance)
            return cameras_info
        except Exception as error:
            raise error



    
    
