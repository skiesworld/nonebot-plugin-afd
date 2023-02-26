from nonebot import get_driver
from .config import Config

config = Config.parse_obj(get_driver().config)

from . import group_new_member
