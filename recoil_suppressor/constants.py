from typing import Dict, List

from device_adapters import DeviceType, DeviceInstruction, MouseEventFlag
from weapon_detector import WeaponIdentity

RECOIL_SUPPRESSION_DICT: Dict[WeaponIdentity, List[DeviceInstruction]] = {
    WeaponIdentity.Unknown: [
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
        (DeviceType.Mouse, ([MouseEventFlag.Move], (0, 5), 0), 0.01),
    ]
}
