import os
from airgym.utils.task_registry import task_registry


try:
    from .base.X152bPx4_config import X152bPx4Cfg
    from .base.X152bPx4 import X152bPx4
    task_registry.register("X152b", X152bPx4, X152bPx4Cfg())
except ImportError:
    print("Warning! X152bPx4_config or X152bPx4 cannot be imported. Ignore if using on real robot inference.")

try:
    from .base.X152bPx4_with_cam_config import X152bPx4WithCamCfg
    from .base.X152bPx4_with_cam import X152bPx4WithCam
    task_registry.register("X152b_with_cam", X152bPx4WithCam, X152bPx4WithCamCfg())
except ImportError:
    print("Warning! X152bPx4WithCamCfg or X152bPx4WithCam cannot be imported. Ignore if using on real robot inference.")

from .base.inference import inference
task_registry.register("inference", inference, X152bPx4Cfg())