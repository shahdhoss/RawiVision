from pydantic import BaseModel

class CameraMetadataBase(BaseModel):
    room: str | None = None
    building: str | None = None
    username: str
    password: str
    rtsp_urls: list[str]
    ip_address: str
    mac_address: str

class CameraMetadataResponse(CameraMetadataBase):
    pass