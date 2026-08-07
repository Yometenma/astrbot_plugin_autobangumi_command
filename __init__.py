"""astrbot_plugin_autobangumi_command — AutoBangumi 遥控插件。"""

from .main import AutoBangumiCommandPlugin, __version__
from .ab_client import ABCLient

__all__ = ["AutoBangumiCommandPlugin", "ABCLient", "__version__"]
