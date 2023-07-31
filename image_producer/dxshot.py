import os
import sys
from typing import TypeAlias

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/libs')


class DxShot:
    # noinspection PyUnresolvedReferences
    from dxshot import DXCamera, create, device_info, output_info


DXCamera: TypeAlias = DxShot.DXCamera
create: TypeAlias = DxShot.create
device_info: TypeAlias = DxShot.device_info
output_info: TypeAlias = DxShot.output_info
