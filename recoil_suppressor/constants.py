from typing import Dict, List, Tuple

from device_adapters import DeviceType, DeviceEvent, MouseEventFlag
from weapon_detector import WeaponIdentity

RECOIL_SUPPRESSION_DICT: Dict[WeaponIdentity, List[Tuple[DeviceType, DeviceEvent, float]]] = {
    WeaponIdentity.R301: [
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
