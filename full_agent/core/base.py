from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

@dataclass
class ComputerInfo:
    os: str
    os_version: str
    platform: str
    architecture: str
    hostname: str
    ip_address: str

    cpu_brand: str
    cpu_cores_physical: int
    cpu_cores_logical: int
    cpu_frequency_mhz: float

    ram: str
    storage: str

    network_interfaces: str
    gpu_name: Optional[str] = None
    gpu_memory: Optional[str] = None

@dataclass
class Process:
    name: str
    os: str
    description: Optional[str] = None
    exe: Optional[str] = None

@dataclass
class Stat:
    cpu_load: float = 0
    ram_load: float = 0
    network_load: float = 0
    # gpu_load: float = 0

@dataclass
class ProcessStat(Stat):
    pid: int = -1
    exe: str = ""
    name: Optional[str] = None
    username: Optional[str] = None
    cmdline: Optional[str] = None

class ResponseType(IntEnum):
    OK = 0b000
    WARNING = 0b001
    SUSPICIOUS_PROCESS = 0b100
    FULL_MEMORY = 0b110
    MANY_INTERNET = 0b111

@dataclass
class MonitoringResponse:
    type: ResponseType
    comment: str = ""
