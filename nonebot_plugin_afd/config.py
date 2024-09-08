from typing import Dict, List

from pydantic import BaseModel, Field


class Config(BaseModel):
    """配置文件"""

    afd_token_dict: Dict[int, List[str]] = Field(default_factory=dict)
