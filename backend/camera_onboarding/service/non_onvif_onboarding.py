from onboarding_interface import OnboardingInterface
import socket
import nmap
import cv2
import subprocess
import re

class NonOnvifOnboarding(OnboardingInterface):
    def __init__(self):
        self.camera_ips=[]
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

    def is_camera(self, ip, username, password):
        for path in self.RTSP_PATHS:
            url = f"rtsp://{username}:{password}@{ip}:554/{path}"
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cap.release()
                    return True
                cap.release()
        return False    

    def get_camera_ip_addresses(self, username, password): # this function is verryyy slow, need to find a solution for that
        network_range = "192.168.1.0/24"
        nm = nmap.PortScanner()
        nm.scan(hosts=network_range, ports='80,443,554,8080,8554', arguments='-sV -T4')
        for host in nm.all_hosts():
            if 'tcp' not in nm[host]:
                continue
            ports = nm[host]['tcp']
            has_rtsp = 554 in ports or 8554 in ports
            has_http = 80 in ports or 8080 in ports
            if (has_rtsp or has_http) and self.is_camera(host, username=username, password=password):
                self.camera_ips.append(host)
        return self.camera_ips

    def discover_camera_mac_address(self, ip, username, password):
        try:
            subprocess.run(["ping", "-c", "1",ip], stdout=subprocess.DEVNULL)
            arp_output = subprocess.check_output(["arp", "-n"]).decode()
            for line in arp_output.split("\n"):
                if ip in line:
                    mac = re.search(r"([0-9a-f]{2}(:[0-9a-f]{2}){5})", line.lower())
                    if mac:
                        mac_address= mac.group(0)
            return mac_address
        except Exception as error:
            raise error
    
    def get_rtsp_url(self, ip, username, password):
        try:
            urls=[]
            for path in self.RTSP_PATHS:
                url = f"rtsp://{username}:{password}@{ip}:554/{path}"
                cap = cv2.VideoCapture(url)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        cap.release()
                        urls.append(url)
                    cap.release()
            return urls
        except Exception as error:
            raise error

    def get_camera_info(self, ip, username, password):
        try:
            camera_info={}
            for ip in self.camera_ips:
                ip_info={}
                mac_address = self.discover_camera_mac_address(ip=ip, username=username, password=password)
                rtsp_urls= self.get_rtsp_url(ip=ip, username=username, password=password)
                ip_info["mac_address"]=mac_address
                ip_info["rtsp_url"] =rtsp_urls
                camera_info[ip]=ip_info
            return camera_info
        except Exception as error:
            raise error