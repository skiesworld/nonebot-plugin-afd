from nonebot import get_plugin_config
from pydantic import BaseModel, Field


class Config(BaseModel):
    """配置文件"""

    afd_token_dict: dict[int, list[str]] = Field(default_factory=dict)


plugin_config = get_plugin_config(Config)
