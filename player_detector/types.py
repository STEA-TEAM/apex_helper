from enum import Enum


class DeviceType(Enum):
    Cpu = "cpu"
    Cuda = "cuda"
    Xpu = "xpu"
