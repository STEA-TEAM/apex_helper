from typing import Dict, List

from device_adapters import DeviceType, DeviceInstruction, MouseEventFlag
from weapon_detector import WeaponIdentity

# For sensitivity 1.0
RECOIL_SUPPRESSION_DICT: Dict[WeaponIdentity, List[DeviceInstruction]] = {
    WeaponIdentity.Havoc: [
        (DeviceType.Idle, None, 0.04),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-16, 38), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-24, 53), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (9, 46), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-4, 43), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (7, 27), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (13, 18), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (4, 29), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (14, 22), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (7, 23), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-4, 18), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-13, 9), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-16, 10), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-16, -6), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-18, 0), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-9, 24), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (5, 14), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (10, 7), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (16, 11), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (14, -4), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (11, 3), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (15, 6), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (2, 25), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-7, 30), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (7, 18), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (9, 17), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 29), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (13, 26), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (18, 15), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (12, 18), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (13, 18), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (2, 22), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-5, 22), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-4, 21), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (4, 20), 0), 0.0893),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (-10, 16), 0), 0.0893),
    ]
}
