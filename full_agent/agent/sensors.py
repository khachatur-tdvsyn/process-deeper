from core.base import ComputerInfo, Stat, ProcessStat
from .settings import PROCESS_INFO_ARRAY

import psutil
import shutil
import platform
import os
import time

from datetime import datetime


def sensor_ram_info():
    virtual_mem = psutil.virtual_memory()
    return {
        'total': virtual_mem.total,
        'avaiable': virtual_mem.available,
        'usage': virtual_mem.used,
        'percent': virtual_mem.percent
    }

def sensor_rom_info():
    disk_usage = shutil.disk_usage("/")
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free,
        'usage': (disk_usage.used / disk_usage.total) * 100
    }

def get_network_average_speed():
    stats = psutil.net_if_stats()
    speed = 0
    for s in stats.values():
        if s.speed != 0:
            speed += s.speed * 1024 * 1024 * 8
    
    return speed

def get_network_usage(interval = 0.01):
    ioc_1 = psutil.net_io_counters()
    time.sleep(interval)
    ioc_2 = psutil.net_io_counters()
    bytes1, bytes2 = (ioc_1.bytes_sent + ioc_1.bytes_recv), (ioc_2.bytes_sent + ioc_2.bytes_recv)
    return abs(bytes2 - bytes1) / interval


def sensor_computer_stat():
    return Stat(
        cpu_load=psutil.cpu_percent(),
        ram_load=psutil.virtual_memory().used,
        network_load=get_network_usage()
    )

def sensor_process_stat():
    processes = []
    #process_iter_arr = ['pid', 'name']
    process_iter_arr = PROCESS_INFO_ARRAY
    for proc in psutil.process_iter(process_iter_arr):
        try:
            # Get rss of memory info if exists
            ram_load = proc.info.get('memory_info') and proc.info.get('memory_info')[0]
            ps = ProcessStat(
                cpu_load=proc.info.get('cpu_percent'),
                ram_load=ram_load, 
                network_load=-1, # Temp
                pid=proc.info['pid'],
                name=proc.info['name'],
                username=proc.info.get('username'),
                exe=proc.info.get('exe'),
                cmdline=proc.info.get('cmdline')
            )
            processes.append(ps)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes