import platform
import psutil
import shutil
import socket

from core.base import ComputerInfo

try:
    import GPUtil
    gpu_available = True
except ImportError:
    gpu_available = False

def get_system_info():
    info = ComputerInfo(
        os=platform.system(),
        os_version=platform.version(),
        platform=platform.platform(),
        architecture=platform.machine(),
        hostname=socket.gethostname(),
        ip_address=socket.gethostbyname(socket.gethostname()),
        cpu_brand=platform.processor(),
        cpu_cores_physical=psutil.cpu_count(logical=False),
        cpu_cores_logical=psutil.cpu_count(logical=True),
        cpu_frequency_mhz=psutil.cpu_freq().current,
        ram = psutil.virtual_memory().total,
        storage=shutil.disk_usage("/").total,
        network_interfaces=", ".join(psutil.net_if_addrs().keys()),
    )


    if gpu_available:
        gpus = GPUtil.getGPUs()
        print(gpus)
        if gpus:
            info.gpu_name = gpus[0].name
            info.gpu_memory = gpus[0].memoryTotal * 1024**2

    return info