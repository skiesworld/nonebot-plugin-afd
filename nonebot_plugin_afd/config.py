from typing import Optional, Dict

from pydantic import BaseModel, Extra, Field


class Config(BaseModel, extra=Extra.ignore):
    afd_token_list: Optional[Dict[str, Dict[str, str]]] = Field(default_factory=dict)
