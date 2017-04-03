import socket
import struct
from fcntl import ioctl


def get_interface_ip(ifname):
    SIOCGIFADDR = 0x8915
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = ioctl(s.fileno(), SIOCGIFADDR, struct.pack('256s', ifname[:15]))
        return socket.inet_ntoa(addr[20:24])
    except:
        return ""


def is_local_ip(ip_str):
    if not ip_str:
        return False

    if ip_str.startswith("10.")\
       or ip_str.startswith("192.")\
       or ip_str.startswith("172."):
        return True

    return False


def _get_local_ip():
    ret = get_interface_ip("eth0")
    if is_local_ip(ret):
        return ret
    ret = get_interface_ip("eth1")
    if is_local_ip(ret):
        return ret
    return "127.0.0.1"

_local_ip = None


def get_local_ip():
    global _local_ip
    if _local_ip is None:
        _local_ip = _get_local_ip()
    return _local_ip

if __name__ == "__main__":
    print get_local_ip()
