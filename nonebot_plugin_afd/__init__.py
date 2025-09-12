from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="爱发电订单号进群审核",
    description="审核入群信息判断是否同意进群",
    usage="给予机器人管理员权限，填写配置信息，当有入群申请时机器人会审核入群信息",
    type="application",
    homepage="https://github.com/17TheWord/nonebot-plugin-afd",
    config=Config,
    supported_adapters={"nonebot.adapters.onebot.v11", "nonebot.adapters.afdian"},
)

from . import group_new_member as group_new_member
from . import order_notice as order_notice

# 初始化全局作者与群关系数据
from .utils import init_global_data

init_global_data()
