from wsdiscovery import WSDiscovery # for onvif-compaitable cameras
import subprocess
import re
from urllib.parse import urlparse
from onboarding_interface import OnboardingInterface
import cv2

class OnvifOnboarding(OnboardingInterface):
    def __init__(self):
        self.camera_ips = []
        self.RTSP_PATHS = [
            "/Streaming/Channels/101",
            "/Streaming/Channels/102",
            "/Streaming/Channels/201",
            "/Streaming/Channels/301",
            "/Streaming/Channels/401",
            "/h264/ch1/main/av_stream",
            "/h264/ch1/sub/av_stream",
            "/live",
            "/live.sdp",
            "/stream1",
            "/stream2",
            "/cam/realmonitor?channel=1&subtype=0"]

    def is_camera(self, types):
        if 'networkvideotransmitter' in str(types).lower(): # i think i need to add more strings, not sure tho
            return True
        return False

    def discover_cameras(self):
        wsd = WSDiscovery()
        wsd.start()
        services = wsd.searchServices(timeout=10) 
        for service in services:
            types = service.getTypes()
            if self.is_camera(types): 
                xaddrs = service.getXAddrs()
                for addr in xaddrs:
                    parsed = urlparse(addr)
                    ip = parsed.hostname
                    self.camera_ips.append(ip)
        wsd.stop()
    
    def discover_mac_address(self, ip):
        try:
            subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL)
            arp_output = subprocess.check_output(["arp", "-n"]).decode()
            for line in arp_output.split("\n"):
                if ip in line:
                    mac = re.search(r"([0-9a-f]{2}(:[0-9a-f]{2}){5})", line.lower())
                    if mac:
                        mac_address = mac.group(0)
            return mac_address
        except Exception as error:
            raise error
    
    def get_camera_ip_addresses(self):
        try:
            self.discover_cameras()
            return self.camera_ips
        except Exception as error:
            raise error
    
    def get_rtsp_url(self, ip, username, password): # even if it is empty streams it is fine, so they could be added dynamically when the streams become alive. But i need to have a check before adding the video chunks to minio
        rtsp_urls = []
        for path in self.RTSP_PATHS:
            url = f"rtsp://{username}:{password}@{ip}:554{path}" 
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    rtsp_urls.append(url)
                cap.release()
        return rtsp_urls

