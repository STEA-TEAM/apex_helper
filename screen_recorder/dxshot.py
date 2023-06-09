import os
import sys
from typing import TypeAlias

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/libs')


class DxShot:
    # noinspection PyUnresolvedReferences
    from dxshot import DXCamera, create


DXCamera: TypeAlias = DxShot.DXCamera
create: TypeAlias = DxShot.create
